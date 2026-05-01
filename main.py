import ollama
import json
import os
import sys

# Change these to your actual file names
IMAGE_PATH = "D:\Grocery\May2026.jpg"
OUTPUT_FILE = "grocery_data.json"
MODEL = "gemma4:e4b"

def extract_bill():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: {IMAGE_PATH} not found.")
        sys.exit(1)

    print(f"Using uv to run extraction on {IMAGE_PATH}...")
    
    # prompt = """
    # Analyze this grocery bill image. Extract the following details into a structured JSON object.
    
    # For each line item, capture: HSN code, Item name, Description, Net Price, Quantity, and final Value.
    # Also extract the Store Name, Bill Date, Bill Number, and Grand Total.

    # Return ONLY a valid JSON object in this exact format:
    # {
    #   "store_name": "string",
    #   "bill_date": "string",
    #   "bill_number": "string",
    #   "items": [
    #     {
    #       "hsn": "string",
    #       "item": "string",
    #       "description": "string",
    #       "net_price": 0.00,
    #       "qty": 0,
    #       "value": 0.00
    #     }
    #   ],
    #   "grand_total": 0.00
    # }
    # """

    prompt = """
    You are a high-precision OCR assistant. 
    Analyze this grocery bill image in three distinct steps:

    STEP 1: Identify the main table columns (HSN, Item/Description, Price, Qty, Value).
    STEP 2: For every line, transcribe the 'Item' and 'Description' EXACTLY as printed. 
            Do not summarize or change abbreviations (e.g., if it says 'APL 1KG', do not write 'Apple').
            If a name is unclear, write [UNCLEAR] instead of guessing.
    STEP 3: Verify that the 'Value' column equals 'Qty' multiplied by 'Net Price'.

    OUTPUT: Return ONLY a valid JSON object. 
    Ensure Bill Date (format: YYYY-MM-DD) and Bill Number are extracted.

    JSON SCHEMA:
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
    """


    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{'role': 'user', 'content': prompt, 'images': [IMAGE_PATH]}],
            options={'temperature': 0}
        )
        
        # Strip potential markdown code blocks
        clean_content = response['message']['content'].strip().strip('`').replace('json\n', '')
        data = json.loads(clean_content)

        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Success! Data saved to {OUTPUT_FILE}")
        print(json.dumps(data, indent=2))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_bill()
