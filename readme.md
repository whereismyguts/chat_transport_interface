# Installation

## 1. Create a virtual environment

`python -m venv venv`

## 2. Activate the virtual environment

On Windows

`venv\Scripts\activate`

On Unix or MacOS

`source venv/bin/activate`

## 3. Install the dependencies

`pip install -r requirements.txt`

## 4. Configuration

Copy the `.env.example` file to a new file named `.env` and fill in your Discord and Telegram bot tokens and chat IDs.

# Usage in code

```
from chat_base import ChatTransportDiscord, ChatTransportTelegram
# start polling Telegram bot
transport = ChatTransportTelegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)`

# or start polling Discord bot
# transport = ChatTransportDiscord(DISCORD_BOT_TOKEN, DISCORD_CHAT_ID)

# start the bot
bot = BusinessLogicController(transport)
asyncio.run(bot.run())
```

# Run the bot from the command line:

### To run the bot from the command line:

`python chat_base.py --telegram`

`python chat_base.py --discord`

# Run the tests

`python -m unittest .\tests_basics.py`
