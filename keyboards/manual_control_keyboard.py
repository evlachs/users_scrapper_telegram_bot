from aiogram import types

set_manual_control_button = types.InlineKeyboardButton('Управлять запуском вручную', callback_data='set_manual')

set_manual_control_keyboard = types.InlineKeyboardMarkup()
set_manual_control_keyboard.add(set_manual_control_button)
