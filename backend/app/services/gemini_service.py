from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)
from tenacity import retry, wait_fixed, stop_after_attempt
from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.bill import BillCreate, ItemBase

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(filename: str) -> str:
    return (_PROMPTS_DIR / filename).read_text(encoding="utf-8")


class GeminiService:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_id = settings.gemini_model_id
        self._extract_receipt_prompt = _load_prompt("extract_receipt.txt")

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    def extract_receipt_data(self, image_bytes: bytes) -> BillCreate:
        logger.info(f"Extracting receipt data using model: {self.model_id}")
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                self._extract_receipt_prompt,
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
