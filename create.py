import os
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv(find_dotenv())

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
PASSWORD_EMAIL = os.getenv('PASSWORD_EMAIL')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
GPT_API_KEY = os.getenv('GPT_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')
ADMIN_ID = os.getenv('ADMIN_ID')
password = os.getenv('PASSWORD')
bot = Bot(token=os.getenv('TOKEN_BOT'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

