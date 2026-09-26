from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main():
    main = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='HELP'),KeyboardButton(text='PROFILE'), KeyboardButton(text='SHOW ALL USERS')]
        ],
        resize_keyboard=True
    )

    return main
    