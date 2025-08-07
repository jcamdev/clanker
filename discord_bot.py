import discord
import requests
import os
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Store conversation history per channel
conversation_history = {}

# API configuration
API_KEY = os.getenv('API_KEY')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
AI_GATEWAY = os.getenv('AI_GATEWAY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT')
MODEL = os.getenv('MODEL')
DRAW_MODEL = os.getenv('DRAW_MODEL')
AUTORAG_NAME = os.getenv('AUTORAG_NAME')
AUTORAG_API_KEY = os.getenv('AUTORAG_API_KEY')

# Construct the API URLs
API_URL = f"https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/{AI_GATEWAY}/workers-ai/{MODEL}"
AUTORAG_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/autorag/rags/{AUTORAG_NAME}/ai-search"
DRAW_API_URL = f"https://gateway.ai.cloudflare.com/v1/{ACCOUNT_ID}/{AI_GATEWAY}/workers-ai/{DRAW_MODEL}"

def call_ai_api(messages):
    """Call the AI API with the conversation messages"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": messages
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
        return f"Error calling AI service"

def call_autorag_api(query):
    """Call the Auto RAG search API with a single query"""
    headers = {
        "Authorization": f"Bearer {AUTORAG_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": query
    }
    
    try:
        response = requests.post(AUTORAG_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract just the response content from the Auto RAG API result
        if 'success' in result and result['success'] and 'result' in result and 'response' in result['result']:
            return result['result']['response']
        else:
            return "Sorry, I couldn't get a proper response from the Auto RAG service."
        
    except requests.exceptions.RequestException as e:
        return f"Error calling Auto RAG service"

def call_draw_ai_api(prompt):
    """Call the Draw AI API to generate an image from a prompt"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt
    }
    
    try:
        response = requests.post(DRAW_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        # Return the raw image data (binary PNG)
        return response.content
        
    except requests.exceptions.RequestException as e:
        return None

def trim_conversation_history(messages, max_length=6):
    """Keep conversation history under max_length, preserving the system prompt"""
    if len(messages) <= max_length:
        return messages
    
    # Keep the system prompt (first message) and the most recent messages
    system_prompt = messages[0]
    recent_messages = messages[-(max_length-1):]
    
    return [system_prompt] + recent_messages

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'Bot is ready and listening for !ask & !d2 & !draw commands')

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
        
        # Get or initialize conversation history for this channel
        channel_id = message.channel.id
        if channel_id not in conversation_history:
            conversation_history[channel_id] = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]
        
        # Add user message to conversation history
        conversation_history[channel_id].append({
            "role": "user",
            "content": user_prompt
        })
        
        # Send typing indicator
        async with message.channel.typing():
            # Call the AI API with full conversation history
            ai_response = call_ai_api(conversation_history[channel_id])
        
        # Add assistant response to conversation history
        conversation_history[channel_id].append({
            "role": "assistant",
            "content": ai_response
        })
        
        # Trim conversation history to keep it under 6 messages
        conversation_history[channel_id] = trim_conversation_history(conversation_history[channel_id])
        
        # Send the response back to the channel
        await message.channel.send(ai_response)
    
    # Check if message starts with !d2
    elif message.content.startswith('!d2 '):
        # Extract the query after "!d2 "
        user_query = message.content[4:].strip()
        
        if not user_query:
            await message.channel.send("Please provide a query after `!d2`. Example: `!d2 What is Dota 2?`")
            return
        
        # Send typing indicator
        async with message.channel.typing():
            # Call the Auto RAG API
            rag_response = call_autorag_api(user_query)
        
        # Send the response back to the channel
        await message.channel.send(rag_response)
    
    # Check if message starts with !draw
    elif message.content.startswith('!draw '):
        # Extract the prompt after "!draw "
        user_prompt = message.content[6:].strip()
        
        if not user_prompt:
            await message.channel.send("Please provide a prompt after `!draw`. Example: `!draw cyberpunk cat`")
            return
        
        # Send typing indicator
        async with message.channel.typing():
            # Call the Draw AI API
            image_data = call_draw_ai_api(user_prompt)
        
        if image_data:
            # Create a Discord file from the image data
            file = discord.File(io.BytesIO(image_data), filename="generated_image.png")
            await message.channel.send(f"Generated image for: **{user_prompt}**", file=file)
        else:
            await message.channel.send("Sorry, I couldn't generate an image. Please try again later.")

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file")
        print("Please add your Discord bot token to the .env file")
    else:
        client.run(DISCORD_TOKEN)