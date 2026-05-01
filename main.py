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

    prompt = """
    Analyze this grocery bill. Extract store name, items (name/price), and total.
    Return ONLY a valid JSON object:
    {
      "store": "string",
      "items": [{"name": "string", "price": 0.00}],
      "total": 0.00
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
