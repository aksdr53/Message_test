import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import aiohttp
import asyncio

API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
WEB_APP_URL = 'http://web:80/api/v1'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I'm your bot. Type /get to see messages or /write to write a message.")

@dp.message_handler(commands=['get'])
async def get_messages(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{WEB_APP_URL}/messages/') as resp:
            messages = await resp.json()
            response_text = "\n".join([f"{msg['author']}: {msg['content']}" for msg in messages])
            await message.reply(response_text)

@dp.message_handler(commands=['write'])
async def write_message(message: types.Message):
    await message.reply("Please send your message in the format: /write <author> <message>")

@dp.message_handler(lambda message: message.text.startswith('/write '))
async def process_write(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.reply("Invalid format. Use: /write <author> <message>")
        return
    author = parts[1]
    content = parts[2]
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{WEB_APP_URL}/message/', json={'author': author, 'content': content}) as resp:
            if resp.status == 200:
                await message.reply("Message saved!")
            else:
                await message.reply("Failed to save message.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)