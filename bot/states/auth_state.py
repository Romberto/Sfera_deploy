from aiogram.dispatcher.filters.state import State, StatesGroup


class AuthState(StatesGroup):

    login = State()
    passwd = State()