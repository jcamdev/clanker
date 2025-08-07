import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get values from environment variables
api_key = os.getenv('API_KEY')
account_id = os.getenv('ACCOUNT_ID')
ai_gateway = os.getenv('AI_GATEWAY')
autorag_name = os.getenv('AUTORAG_NAME')
autorag_api_key = os.getenv('AUTORAG_API_KEY')

# regular model search
url = f"https://gateway.ai.cloudflare.com/v1/{account_id}/{ai_gateway}/workers-ai/@cf/meta/llama-3.1-8b-instruct"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Provide clear and informative responses."
        },
        {
            "role": "user",
            "content": "What is Cloudflare?"
        }
    ]
}

#auto rag search
url2 = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/autorag/rags/{autorag_name}/ai-search"

headers2 = {
    "Authorization": f"Bearer {autorag_api_key}",
    "Content-Type": "application/json"
}

data2 = {
    "query": "What is Dota 2?"
}


try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print(response.json())
    response2 = requests.post(url2, headers=headers2, json=data2)
    response2.raise_for_status()
    print(response2.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")