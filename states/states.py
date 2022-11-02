from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    active_group = State()
    active_channel = State()
    delay = State()
    launch_time = State()
    limit = State()
