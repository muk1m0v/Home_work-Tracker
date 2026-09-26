from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main():
    main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='HELP'),KeyboardButton(text='ABOUT ME')]
    ],
    resize_keyboard=True
)