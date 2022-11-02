from aiogram import types
from aiogram.dispatcher import FSMContext

from states import Form
from loader import dp, bot
from messages import MESSAGES
from scrapping_manage import SettingsManage
from keyboards import settings_launch_keyboard


@dp.callback_query_handler(lambda c: c.data == 'set_manual', state=Form.launch_time)
async def set_manual_control(callback_query: types.CallbackQuery, state: FSMContext):
    sm = SettingsManage()
    async with state.proxy() as data:
        data['launch_time'] = False
        sm.active_channel = data['active_channel']
        sm.active_group = data['active_group']
        sm.limit = data['limit']
        sm.delay = data['delay']
        sm.launch_time = data['launch_time']
    await state.finish()
    await bot.send_message(
        callback_query.from_user.id,
        MESSAGES['start_scrapping'],
        reply_markup=settings_launch_keyboard()
    )
