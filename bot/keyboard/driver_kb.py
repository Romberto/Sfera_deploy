from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_drivers = ReplyKeyboardMarkup([
    [
        KeyboardButton('Проверить код'),
        KeyboardButton('Отчёт за сегодня')
    ],
    [
        KeyboardButton('/start')
    ],
], resize_keyboard=True, one_time_keyboard=True)