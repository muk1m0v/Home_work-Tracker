from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject 
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    await message.answer(f'Welcome, {user.full_name}!')

@router.message()
async def other(message: Message):
    user = message.from_user
    await message.answer(f'{user.username}: {message.text}\n\nBot: Можно по человечески?!')