import os
import random
from aiogram import Bot, Dispatcher, types
from aogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
responces = [
    'helllo!',
    'Welcome to Gilford!'
]

@dp.message_handler()
async def handle_message(message: Message):
    reply = random.choice(responces)
    await message.answer(reply)


if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp)