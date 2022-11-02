from aiogram import types

from loader import dp, bot
from messages import MESSAGES
from keyboards import set_settings_keyboard


@dp.message_handler(commands=['start', 'help'])
async def start_message_processing(message: types.Message):
    await bot.send_message(message.chat.id, MESSAGES['start'], reply_markup=set_settings_keyboard)
    with open('data/users_id.txt', 'r+') as file:
        if not str(message.chat.id) in file.read().split('\n'):
            file.seek(0, 2)
            file.write(str(message.chat.id)+'\n')
