import discord
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# API configuration
API_KEY = os.getenv('API_KEY')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
AI_GATEWAY = os.getenv('AI_GATEWAY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT')

# Construct the API URL
API_URL = f"https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/{AI_GATEWAY}/workers-ai/@cf/meta/llama-3.1-8b-instruct"

def call_ai_api(user_prompt):
    """Call the AI API with the user's prompt"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract the response from the API result
        if 'result' in result and 'response' in result['result']:
            return result['result']['response']
        else:
            return "Sorry, I couldn't get a proper response from the AI service."
            
    except requests.exceptions.RequestException as e:
        return f"Error calling AI service: {str(e)}"

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'Bot is ready and listening for !ask commands')

@client.event
async def on_message(message):
    # Don't respond to the bot's own messages
    if message.author == client.user:
        return
    
    # Check if message starts with !ask
    if message.content.startswith('!ask '):
        # Extract the prompt after "!ask "
        user_prompt = message.content[5:].strip()
        
        if not user_prompt:
            await message.channel.send("Please provide a question after `!ask`. Example: `!ask what is cloudflare?`")
            return
        
        # Send typing indicator
        async with message.channel.typing():
            # Call the AI API
            ai_response = call_ai_api(user_prompt)
        
        # Send the response back to the channel
        await message.channel.send(ai_response)

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file")
        print("Please add your Discord bot token to the .env file")
    else:
        client.run(DISCORD_TOKEN)