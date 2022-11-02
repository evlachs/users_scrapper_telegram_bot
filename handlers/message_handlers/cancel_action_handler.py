from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from messages import MESSAGES


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_action(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, MESSAGES['canceled'])
