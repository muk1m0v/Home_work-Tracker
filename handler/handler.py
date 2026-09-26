from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject 
from aiogram.types import Message
from board import main

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    text = f'Welcome, **{user.full_name}**!'
    await message.answer(text, parse_mode='Markdowm', reply_markup=main())

@router.message()
async def other(message: Message):
    user = message.from_user
    await message.answer(f'{user.username}: {message.text}\n\nBot: Можно по человечески?!')