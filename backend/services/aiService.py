import requests
import json

API_KEY = "f52b43fd6b8478407b24bac6fe48949b.VUGM6HOmH2Ryp3Cj"
API_ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


def create_request_body(model, messages):
    request_body = {
        "model": model,
        "messages": messages,
        "temperature": 0.95,
        "max_tokens": 1024
    }
    return json.dumps(request_body)


def send_post_request(request_body):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.post(API_ENDPOINT, headers=headers, data=request_body)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"HTTP error code: {response.status_code}")


def get_content(response):
    try:
        choice = response["choices"][0]
        message = choice["message"]
        return message["content"]
    except KeyError as e:
        raise RuntimeError(f"Error parsing JSON response: {e}")


def connect(request):
    messages = [
        {"role": "user", "content": f"{request}"}
    ]
    request_body = create_request_body("glm-4-flash", messages)
    response = send_post_request(request_body)
    return get_content(response)

def communicate(name, description, request):
    messages = [
        {"role": "system", "content": f"You are {name}. {description}.You need to answer as {name}. Answer no more than three sentences at a time."},
        {"role": "user", "content": f"{request}"}
    ]
    request_body = create_request_body("glm-4-flash", messages)
    response = send_post_request(request_body)
    return get_content(response)
