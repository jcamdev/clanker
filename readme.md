# Discord LLM Bot

A Discord bot that integrates with Cloudflare Workers AI to provide conversational AI responses with persistent conversation memory.

## Features

- Conversational AI powered by Cloudflare Workers AI (Llama 3.1 8B)
- Maintains conversation context (remembers previous messages)
- Smart memory management (keeps last 6 messages + system prompt)
- Secure environment variable configuration
- Simple `!ask` command interface

## Prerequisites

- Python 3.7 or higher
- A Discord account
- A Cloudflare account with Workers AI access

## Discord Bot Setup

### 1. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" section in the left sidebar
4. Click "Add Bot" to create a bot user
5. Under the "Token" section, click "Copy" to get your bot token (save this for later)

### 2. Configure Bot Permissions

1. In the "Bot" section, scroll down to "Privileged Gateway Intents"
2. Enable "Message Content Intent" (required for the bot to read message content)
3. Navigate to the "OAuth2" > "URL Generator" section
4. Under "Scopes", select:
   - `bot`
5. Under "Bot Permissions", select:
   - `Send Messages`
   - `Read Message History`

### 3. Invite Bot to Your Server

1. Copy the generated URL from the OAuth2 URL Generator
2. Open the URL in your browser
3. Select the server you want to add the bot to
4. Click "Authorize"
5. Complete any CAPTCHA if prompted

## Cloudflare Setup

### 1. Get Your Cloudflare Credentials

1. Log in to your [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Go to "AI" > "Workers AI" in the sidebar
3. Note your Account ID (found in the right sidebar)
4. Create an API token:
   - Go to "My Profile" > "API Tokens"
   - Click "Create Token"
   - Use the "Custom token" template
   - Give it a name and set permissions for Workers AI
5. Set up an AI Gateway (optional but recommended):
   - Go to "AI" > "AI Gateway"
   - Create a new gateway and note the gateway name

## Installation & Configuration

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd discord-llm-bot
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Discord Bot Token (from Discord Developer Portal)
DISCORD_TOKEN=your_discord_bot_token_here

# Cloudflare Credentials
API_KEY=your_cloudflare_api_key_here
ACCOUNT_ID=your_cloudflare_account_id_here
AI_GATEWAY=your_ai_gateway_name_here
MODEL=ai_model e.g. @cf/meta/llama-3.1-8b-instruct

# System Prompt (customize the bot's personality)
SYSTEM_PROMPT=You are a helpful AI assistant. Provide clear, concise, and informative responses.
```

### 3. Run the Bot

```bash
python discord_bot.py
```

You should see:
```
[Bot Username] has connected to Discord!
Bot is ready and listening for !ask commands
```

## Usage

### Basic Commands

- `!ask <your question>` - Ask the AI a question
- The bot maintains conversation context, so you can ask follow-up questions

### Examples

```
!ask What is Python?
!ask How do I install it?
!ask What are some good Python libraries for web development?
```

## Configuration Options

### Customizing the System Prompt

Edit the `SYSTEM_PROMPT` in your `.env` file to change the bot's personality:

```env
SYSTEM_PROMPT=You are a coding assistant specializing in Python. Always provide code examples when relevant.
```

### Memory Management

The bot automatically manages conversation memory:
- Keeps the last 6 messages per Discord channel
- Always preserves the system prompt
- Each Discord channel has its own conversation thread

## Contributing

Feel free to submit issues and enhancement requests!
