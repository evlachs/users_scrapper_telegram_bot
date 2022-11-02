import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from telethon.sync import TelegramClient

from conf import BOT_TOKEN, API_ID, API_HASH, PHONE

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')

client = TelegramClient(PHONE, API_ID, API_HASH)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
