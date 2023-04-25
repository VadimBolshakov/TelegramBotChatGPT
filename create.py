import os
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv(find_dotenv())

id = os.getenv('GPT_API_KEY')
password = os.getenv('PASSWORD')
bot = Bot(token=os.getenv('TOKEN_BOT'))
#CHAT_ID = os.getenv('CHAT_ID')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

