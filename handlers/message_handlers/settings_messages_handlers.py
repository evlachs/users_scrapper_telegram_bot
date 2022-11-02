from aiogram import types
from aiogram.dispatcher import FSMContext

from states import Form
from loader import dp, bot, client
from messages import MESSAGES
from scrapping_manage import SettingsManage
from scrapper import UsersScrapper
from keyboards import groups_keyboard, settings_launch_keyboard, set_manual_control_keyboard


@dp.message_handler(commands=['set_settings'])
@dp.message_handler(lambda msg: msg.text in ['Настроить парсинг', 'Обновить настройки'])
async def update_scrapping_settings(message: types.Message):
    sm = SettingsManage
    sm.scrap_mode = False
    await Form.active_channel.set()
    await bot.send_message(message.chat.id, MESSAGES['set_active_channel'])


@dp.message_handler(state=Form.active_channel)
async def set_active_channel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['active_channel'] = message.text
    await Form.active_group.set()
    await bot.send_message(message.chat.id, MESSAGES['set_active_group'], reply_markup=await groups_keyboard())


@dp.message_handler(state=Form.active_group)
async def set_active_group(message: types.Message, state: FSMContext):
    sm = SettingsManage()
    async with state.proxy() as data:
        data['active_group'] = message.text
        if sm.active_group != message.text:
            UsersScrapper(client).clear_users_data()
    await Form.limit.set()
    await bot.send_message(message.chat.id, MESSAGES['set_limit'])


@dp.message_handler(state=Form.limit)
async def set_limit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['limit'] = message.text
    await Form.delay.set()
    await bot.send_message(message.chat.id, MESSAGES['set_delay'])


@dp.message_handler(state=Form.delay)
async def set_delay(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delay'] = message.text
    await Form.launch_time.set()
    await bot.send_message(message.chat.id, MESSAGES['set_launch_time'], reply_markup=set_manual_control_keyboard)


@dp.message_handler(state=Form.launch_time)
async def set_launch_time(message: types.Message, state: FSMContext):
    sm = SettingsManage()
    async with state.proxy() as data:
        data['launch_time'] = message.text
        sm.active_channel = data['active_channel']
        sm.active_group = data['active_group']
        sm.limit = data['limit']
        sm.delay = data['delay']
        sm.launch_time = data['launch_time']
    await state.finish()
    await bot.send_message(message.chat.id, MESSAGES['start_scrapping'], reply_markup=settings_launch_keyboard())
