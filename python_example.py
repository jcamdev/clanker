import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get values from environment variables
api_key = os.getenv('API_KEY')
account_id = os.getenv('ACCOUNT_ID')
ai_gateway = os.getenv('AI_GATEWAY')

# Construct the URL
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

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")