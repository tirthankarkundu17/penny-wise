import ollama
import json
import os
import sys

# Change these to your actual file names
IMAGE_PATH = "D:\Grocery\May2026.jpg"
OUTPUT_FILE = "grocery_data.json"
MODEL = "gemma4:latest"

def extract_bill():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: {IMAGE_PATH} not found.")
        sys.exit(1)

    print(f"Using uv to run extraction on {IMAGE_PATH}...")

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


    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{'role': 'user', 'content': prompt, 'images': [IMAGE_PATH]}],
            options={'temperature': 0.1, 'response_format': 'json'}
        )
        
        # Strip potential markdown code blocks
        clean_content = response['message']['content'].strip().strip('`').replace('json\n', '')
        print("Raw response content:")
        print(clean_content)
        data = json.loads(clean_content)

        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Success! Data saved to {OUTPUT_FILE}")
        print(json.dumps(data, indent=2))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_bill()
