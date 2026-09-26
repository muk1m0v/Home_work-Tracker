from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject 
from aiogram.types import Message
from board import main
from service import *

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    is_login = await check_users(user.id)
    if not is_login:
        await save_user(user.id, user.username, user.full_name)
    else:
        text = f'Welcome, <b>{user.full_name}</b>'
        await message.answer(text, parse_mode='HTML', reply_markup=main())

@router.message(F.text == 'SHOW ALL USERS')
@router.message(Command('show_users'))
async def other(message: Message):
    users = await get_users()
    if not users:
            await message.answer('Пока нет пользователей!')
    else:
        text = 'Users:\n'
        for i in users:
            text += f'ID: {i['id']} | Username: {i['username']} | {i['full_name']}'
        await message.answer(text)

@router.message(F.text == 'HELP')
@router.message(Command('help'))
async def help(message: Message):
    await message.answer('Это бот HOMEWORK TRACKER\n\n')

@router.message(F.text == 'PROFILE')
@router.message(Command('profile'))
async def profile(message: Message):
    user = message.from_user
    await message.answer(f'{user.full_name}\n\nID: {user.id} \nUsername: @{user.username}')

@router.message()
async def other(message: Message):
    user = message.from_user
    await message.answer(f'{user.username}: {message.text}\n\nBot: Можно по человечески')