import unittest
from unittest.mock import patch, AsyncMock
import asyncio
import os
from chat_base import ChatTransportDiscord, ChatTransportTelegram, BusinessLogicController

# Helper function for running async tests


def async_test(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f(*args, **kwargs))
    return wrapper


class TestBusinessLogicControllerDiscord(unittest.TestCase):
    def setUp(self):
        self.transport = AsyncMock(spec=ChatTransportDiscord)
        self.blc = BusinessLogicController(self.transport)

    @async_test
    async def test_handle_message(self):
        await self.blc.handle_message("Hello")
        self.transport.send_message.assert_awaited_with('Hi! Your message was received: "Hello"')


class TestBusinessLogicControllerTelegram(unittest.TestCase):
    def setUp(self):
        self.transport = AsyncMock(spec=ChatTransportTelegram)
        self.blc = BusinessLogicController(self.transport)

    @async_test
    async def test_handle_message(self):
        await self.blc.handle_message("Hello")
        self.transport.send_message.assert_awaited_with('Hi! Your message was received: "Hello"')


class TestSystem(unittest.TestCase):
    @patch.dict(os.environ, {'TELEGRAM_BOT_TOKEN': 'fake_token', 'TELEGRAM_CHAT_ID': '123', 'DISCORD_BOT_TOKEN': 'fake_token', 'DISCORD_CHANNEL_ID': '123'})
    def test_environment_variables(self):
        self.assertEqual(os.getenv('TELEGRAM_BOT_TOKEN'), 'fake_token')
        self.assertEqual(os.getenv('TELEGRAM_CHAT_ID'), '123')
        self.assertEqual(os.getenv('DISCORD_BOT_TOKEN'), 'fake_token')
        self.assertEqual(os.getenv('DISCORD_CHANNEL_ID'), '123')
        print('Environment variables are set correctly')


if __name__ == '__main__':
    unittest.main()
