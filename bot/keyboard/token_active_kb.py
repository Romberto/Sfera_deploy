from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb_tokens = ReplyKeyboardMarkup([
    [
        KeyboardButton('Активировать'),
        KeyboardButton('Назад')
    ],
], resize_keyboard=True, one_time_keyboard=True)

