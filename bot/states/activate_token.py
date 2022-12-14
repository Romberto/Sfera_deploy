from aiogram.dispatcher.filters.state import State, StatesGroup


class ActivateTokenState(StatesGroup):
    start = State()
    token = State()
    token_active = State()
    token_finish = State()
