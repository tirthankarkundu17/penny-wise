import httpx
import os

def test_upload():
    url = "http://127.0.0.1:8000/upload"
    image_path = "D:\\Grocery\\May2026.jpg" # From the user's script
    
    if not os.path.exists(image_path):
        print(f"Image not found at {image_path}. Please provide a valid path.")
        return

    with open(image_path, "rb") as f:
        files = {"file": ("receipt.jpg", f, "image/jpeg")}
        response = httpx.post(url, files=files)
        
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Upload successful!")
        print(response.json())
    else:
        print(f"Error: {response.text}")

def test_list_bills():
    url = "http://127.0.0.1:8000/bills"
    response = httpx.get(url)
    print(f"Bills: {response.json()}")

if __name__ == "__main__":
    # Note: Ensure the server is running before executing this
    test_upload()
    test_list_bills()
