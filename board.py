from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main():
    main = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='HELP'),KeyboardButton(text='PROFILE')]
        ],
        resize_keyboard=True
    )

    return main
    