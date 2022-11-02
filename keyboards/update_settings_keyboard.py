from aiogram import types

from scrapping_manage import SettingsManage


def settings_launch_keyboard():
    update_settings_button = types.KeyboardButton('Обновить настройки')
    stop_parsing_button = types.KeyboardButton('Остановить парсинг')
    launch_parsing_button = types.KeyboardButton('Запустить парсинг')
    change_settings_launch_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sm = SettingsManage()
    if sm.scrapping_status:
        change_settings_launch_keyboard.add(update_settings_button, stop_parsing_button)
    else:
        change_settings_launch_keyboard.add(update_settings_button, launch_parsing_button)
    return change_settings_launch_keyboard

