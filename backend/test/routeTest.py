import os

import requests

from backend.config import basedir

BASE_URL = "http://127.0.0.1:5000"


def test_register():
    print("\nTesting Register Endpoint")
    payload = {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com",
        "pic_url": "test_image_1742704145.jpg"
    }
    response = requests.post(f"{BASE_URL}/register", data=payload)
    print("Response:", response.status_code, response.text)


def test_login():
    print("\nTesting Login Endpoint")
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/login", data=payload)
    print("Response:", response.status_code, response.text)
    return response.json().get("access_token")


def test_profile(access_token):
    print("\nTesting Profile Endpoint")
    headers = {"Authorization": f"Bearer {access_token}"}

    # get
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    print("Response (GET):", response.status_code, response.text)

    # put
    payload = {"email": "updatedtest@example.com", "pic_url": "updated_test_image_1742704145.jpg"}
    response = requests.put(f"{BASE_URL}/profile", headers=headers, data=payload)
    print("Response (PUT):", response.status_code, response.text)


def test_crud(access_token):
    print("\nTesting CRUD Endpoint")
    headers = {"Authorization": f"Bearer {access_token}"}

    # POST
    payload = {"user_id": 1, "message": "This is a test"}
    response = requests.post(f"{BASE_URL}/crud/RemembranceMessage", headers=headers, data=payload)
    print("Response (POST):", response.status_code, response.text)

    # POST creat memorial hall
    payload = {"name": 'testDeceased', "creator_id": "1"}
    # Set the path to the image file you want to upload
    file_path = os.path.join(basedir, 'test', 'test_image.jpg')

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        exit()

    # Open the file and prepare to send it
    with open(file_path, 'rb') as f:
        files = {'pic': (os.path.basename(file_path), f, 'image/jpeg')}  # Adjust MIME type according to file type
        response = requests.post(f"{BASE_URL}/crud/Deceased", headers=headers, data=payload,files=files)
    print("Response (POST):", response.status_code, response.text)

    # GET
    payload = {"id": 1}
    response = requests.get(f"{BASE_URL}/crud/RemembranceMessage", headers=headers, params=payload)
    print("Response (GET):", response.status_code, response.text)

    # PUT
    payload = {"id": 1, "message": "Updated description"}
    response = requests.put(f"{BASE_URL}/crud/RemembranceMessage", headers=headers, data=payload)
    print("Response (PUT):", response.status_code, response.text)

    test_invite(access_token)

    # DELETE
    payload = {"id": 1}
    response = requests.delete(f"{BASE_URL}/crud/User", headers=headers, data=payload)
    print("Response (DELETE):", response.status_code, response.text)


def test_invite(access_token):
    print("\nTesting Invite Endpoint")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/memorial/1/invite", headers=headers)
    print("Response (POST):", response.status_code, response.text)


def test_ai(access_token):
    print("\nTesting ai Endpoint")
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"text": "介绍一下自己"}
    response = requests.post(f"{BASE_URL}/ai", headers=headers, data=payload)
    print("Response (POST):", response.status_code, response.text)


def test_lunar():
    print("\nTesting Lunar Calendar Endpoint")
    response = requests.get(f"{BASE_URL}/lunar")
    print("Response (GET):", response.status_code, response.text)


if __name__ == "__main__":
    test_lunar()

    test_register()

    access_token = test_login()

    if access_token:
        test_profile(access_token)
        test_crud(access_token)
        # test_ai(access_token)