from aiogram.dispatcher.filters.state import State, StatesGroup


class ReportState(StatesGroup):
    start = State()
