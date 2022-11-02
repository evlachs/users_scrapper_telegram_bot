from aiogram.types import BotCommand


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            BotCommand('set_settings', 'установить/обновить настройки'),
            BotCommand('cancel', 'отменить действие'),
        ]
    )
