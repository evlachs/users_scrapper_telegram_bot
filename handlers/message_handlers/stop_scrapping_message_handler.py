from aiogram import types

from loader import dp, bot
from messages import MESSAGES
from keyboards import settings_launch_keyboard

from scrapping_manage import SettingsManage


@dp.message_handler(lambda msg: msg.text == 'Остановить парсинг')
async def start_parsing(message: types.Message):
    sm = SettingsManage()
    sm.scrapping_status = False
    await bot.send_message(message.chat.id, MESSAGES['scrapping_stopped'], reply_markup=settings_launch_keyboard())
