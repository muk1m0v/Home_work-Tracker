from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main():
    main = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='HELP'),KeyboardButton(text='PROFILE'), KeyboardButton(text='SHOW ALL USERS'),KeyboardButton(text='MENU')]
        ],
        resize_keyboard=True
    )

    return main

def menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📊 Мои оценки'),KeyboardButton(text='Выпольнить Задание')],
            [KeyboardButton(text='Добавить Задание'),KeyboardButton(text='Мои задание')],
            [KeyboardButton(text='Поставить оценку'),KeyboardButton(text='Моя Сред.Оценка')],
        ],
        resize_keyboard=True
    )

    return menu