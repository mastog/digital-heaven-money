
import requests
import json

def get_access_token():
    """
    使用应用API Key，应用Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MfFBcU2nXc2EPk6J2qKg1laG&client_secret=VacNiEz5JzNaLHznZ1d6Pwltiv5z4Wyx"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def main():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "历史上的今天有哪些名人出生或者去世？请列出五个左右，回答且仅回答他们的名字，职业和出生或者去世的日期，不要有任何其他内容，回答全程使用英文，不要出现中文"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

if __name__ == '__main__':
    main()