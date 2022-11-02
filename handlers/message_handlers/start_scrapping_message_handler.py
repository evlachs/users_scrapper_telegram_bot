from aiogram import types

from loader import dp, bot
from messages import MESSAGES
from keyboards import settings_launch_keyboard

from scrapping_manage import SettingsManage


@dp.message_handler(lambda msg: msg.text == 'Запустить парсинг')
async def start_parsing(message: types.Message):
    sm = SettingsManage()
    sm.scrapping_status = True
    await bot.send_message(message.chat.id, MESSAGES['collect_data'], reply_markup=settings_launch_keyboard())
