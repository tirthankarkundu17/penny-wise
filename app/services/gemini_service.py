from google import genai
from google.genai import types
import json
from tenacity import retry, wait_fixed, stop_after_attempt

from app.core.config import settings
from app.schemas.bill import BillCreate, ItemBase


class GeminiService:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_id = "gemini-2.5-flash"

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    def extract_receipt_data(self, image_bytes: bytes) -> BillCreate:
        prompt = """
        Transcribe the following details from this bill image into a JSON object.
        Fields to extract: Store Name, Bill Date, Bill Number, Grand Total.
        For each item, extract: HSN Code, Item Name, Description, Net Price, Quantity (Qty), and Value.

        Strictly follow this JSON schema:
        {
          "store_name": "string",
          "bill_date": "string",
          "bill_number": "string",
          "items": [
            {
              "hsn": "string",
              "item_name": "string",
              "description": "string",
              "net_price": 0.00,
              "qty": 0.0,
              "value": 0.00
            }
          ],
          "grand_total": 0.00
        }

        Important:
        - If HSN is missing for an item, leave it as null.
        - Do not guess names; if unclear, mark as [UNCLEAR].
        - Ensure 'value' equals 'qty' multiplied by 'net_price'.
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json", temperature=0.1
            ),
        )

        data = json.loads(response.text)

        items = [
            ItemBase(
                hsn=it.get("hsn"),
                item_name=it.get("item_name") or it.get("item", "[UNKNOWN]"),
                description=it.get("description"),
                net_price=float(it.get("net_price", 0)),
                qty=float(it.get("qty", 0)),
                value=float(it.get("value", 0)),
            )
            for it in data.get("items", [])
        ]

        return BillCreate(
            store_name=data.get("store_name", "Unknown Store"),
            bill_date=data.get("bill_date", "Unknown Date"),
            bill_number=data.get("bill_number"),
            grand_total=float(data.get("grand_total", 0)),
            items=items,
        )
