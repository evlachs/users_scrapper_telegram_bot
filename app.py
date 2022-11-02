import asyncio

from aiogram import executor

from loader import dp, client
from utils import set_default_commands, launch_inviting
from conf import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_PORT, WEBAPP_HOST
import handlers


async def on_startup(dispatcher):
    """Sets default commands for the bot, initializes the client, launches the loop with the invite_users function"""
    await set_default_commands(dispatcher)
    await client.start()
    loop = asyncio.get_event_loop()
    loop.create_task(launch_inviting())
    await dp.bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()

if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
