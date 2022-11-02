from aiogram import types

set_settings_button = types.KeyboardButton('Настроить парсинг')

set_settings_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
set_settings_keyboard.add(set_settings_button)
