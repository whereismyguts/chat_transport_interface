from abc import ABC, abstractmethod
import discord
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode


# TODO move to separate files
# TODO add logging

class ChatTransport(ABC):
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.handlers = {}

    def add_handler(self, event, handler):
        self.handlers[event] = handler

    @abstractmethod
    async def send_message(self, msg):
        pass

    @abstractmethod
    async def run(self):
        pass


class ChatTransportDiscord(ChatTransport):
    def __init__(self, token, channel_id):
        super().__init__(channel_id)
        #  intents = discord.Intents.all()
        intents = discord.Intents(
            message_content=True,
            messages=True,
            guilds=True,
        )
        self.client = discord.Client(intents=intents)
        self.channel_id = channel_id
        self.token = token

    async def send_message(self, msg):
        try:
            channel = self.client.get_channel(int(self.channel_id))
            await channel.send(msg)
        except Exception as e:
            print(f"Failed to send message on Discord: {e}")

    async def run(self):
        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user.name}')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            handler = self.handlers.get('message')  # TODO event types
            if handler:
                await handler(message.content)

        await self.client.start(self.token)


class ChatTransportTelegram(ChatTransport):
    def __init__(self, token, chat_id):
        super().__init__(chat_id)
        self.bot = Bot(token)
        self.dp = Dispatcher()

    async def send_message(self, msg_text):
        # todo add msg ojbect to proper reply
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=msg_text)
        except Exception as e:
            print(f"Failed to send message on Telegram: {e}")

    async def run(self):
        @self.dp.message()
        async def echo_handler(message: types.Message) -> None:
            handler = self.handlers.get('message')  # #TODO event types
            if handler:
                await handler(message.text)

        await self.dp.start_polling(self.bot, skip_updates=True)


class BusinessLogicController:
    def __init__(self, transport):
        self.transport = transport
        self.transport.add_handler('message', self.handle_message)  # TODO handler types

    async def handle_message(self, msg):
        print(f'BusinessLogicController ({self.transport}): message received: {msg}')
        response = f'Hi! Your message was received: "{msg}"'
        await self.transport.send_message(response)

    async def run(self):
        await self.transport.run()


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    telegram_bot_token = os.getenv('telegram_bot_token')
    telegram_chat_id = os.getenv('telegram_chat_id')

    discord_bot_token = os.getenv('discord_bot_token')
    discord_channel_id = os.getenv('discord_channel_id')

    # discord
    # transport = ChatTransportDiscord(discord_bot_token, discord_channel_id)

    # telegram
    transport = ChatTransportTelegram(telegram_bot_token, telegram_chat_id)

    bot = BusinessLogicController(transport)
    asyncio.run(bot.run())
