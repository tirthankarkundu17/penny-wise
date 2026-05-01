from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv
from tenacity import retry, wait_fixed, stop_after_attempt

load_dotenv()  # Load environment variables from .env file

# CONFIGURATION
API_KEY = os.getenv("GEMINI_API_KEY")
IMAGE_PATH = "D:\\Grocery\\May2026.jpg"
MODEL_ID = "gemini-2.5-flash"  # Use "gemini-1.5-pro" for even higher accuracy

print(f"Using model: {MODEL_ID}")
print(f"Processing image: {IMAGE_PATH}")
print("Initializing Gemini client...", API_KEY[:4] + "****" + API_KEY[-4:])
client = genai.Client(api_key=API_KEY)

@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def extract_data():
    # Structured Prompt for specific billing fields
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
          "item": "string",
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

    # Load and process the image
    with open(IMAGE_PATH, "rb") as f:
        image_bytes = f.read()

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",  # Forces JSON output
                temperature=0.1
            )
        )

        data = json.loads(response.text)
        print(json.dumps(data, indent=2))
        
        with open("extracted_data.json", "w") as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
  extract_data()
