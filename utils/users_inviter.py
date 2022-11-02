import asyncio

from typing import Union

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from datetime import datetime

from messages import MESSAGES
from loader import bot, client
from keyboards import settings_launch_keyboard
from scrapper import UsersScrapper
from scrapping_manage import SettingsManage


async def message_mailing(message: str, keyboard: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]) -> None:
    """
    Sends a message to the client about the start of scrapping or its termination

    :param message: message text
    :type message: str

    :param keyboard: keyboard that will be added to the message
    :type keyboard: aiogram.types.InlineKeyboardMarkup | aiogram.types.ReplyKeyboardMarkup
    """
    with open('data/users_id.txt', 'r') as f:
        users_ids = f.readlines()
        for user in users_ids:
            await bot.send_message(
                user,
                message,
                reply_markup=keyboard
            )


async def invite_users(sm: SettingsManage) -> None:
    """
    Collects users from the group selected by the client and invites them to the specified channel,
    then updates the invited status of the invited users in users.csv
    """
    await message_mailing(MESSAGES['scrapping_started'], settings_launch_keyboard())
    us = UsersScrapper(client)
    target_group = sm.active_group
    groups = await us.get_groups()
    participants = await us.get_chat_participants(groups[target_group])
    us.save_new_users_to_csv(participants)
    to_invite = us.get_users_to_invite()
    if len(to_invite) < sm.limit:
        limit = len(to_invite)
    else:
        limit = sm.limit
    for user in to_invite[:limit]:
        await asyncio.sleep(sm.delay)
        invited_users = await us.invite_users(sm.active_channel, [user])
        us.update_users_status(invited_users)
    if not sm.launch_time:
        sm.scrapping_status = False
    await message_mailing(MESSAGES['scrapping_stopped'], settings_launch_keyboard())


async def launch_inviting() -> None:
    while True:
        now = datetime.now().strftime('%H:%M')
        sm = SettingsManage()
        if (sm.launch_time == now) or (not sm.launch_time and sm.scrapping_status):
            await invite_users(sm)
        await asyncio.sleep(60)
