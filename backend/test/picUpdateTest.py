import requests
import os

# Set the target URL
from backend.config import basedir

url = 'http://localhost:5000/upload_pic'

# Set the path to the image file you want to upload
file_path = os.path.join(basedir,'test','test_image.jpg')

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File does not exist: {file_path}")
    exit()

# Open the file and prepare to send it
with open(file_path, 'rb') as f:
    files = {'pic': (os.path.basename(file_path), f, 'image/jpeg')}  # Adjust MIME type according to file type

    # Send POST request
    response = requests.post(url, files=files)

# Print the response result
print(f"Status code: {response.status_code}")
print("Response content:")
print(response.json())