from aiogram import types

from scrapper import UsersScrapper

from loader import client


async def groups_keyboard():
    select_group_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    us = UsersScrapper(client)
    groups = await us.get_groups()
    for group in groups.keys():
        group_title_button = types.KeyboardButton(group)
        select_group_keyboard.add(group_title_button)
    return select_group_keyboard
