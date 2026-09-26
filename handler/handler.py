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
    
    text = f'Welcome, <b>{user.full_name}</b>'
    await message.answer(text, parse_mode='HTML', reply_markup=main())

@router.message(Command("submit"))
async def submit(message: Message, command: CommandObject):
    user = message.from_user
    sub = command.args
    completed = await new_submit(user.id, sub)
    if not completed:
        await message.answer(F'У вас нет задачи с ID: {sub}')
    else:
        await message.answer(f'Вы сдали задани: {sub}')


@router.message(Command('my_grade'))
async def grades(message: Message):
    user = message.from_user
    grade = await my_grades(user.id)
    find = await found_task()
    if not grade:
        await message.answer('У вас пока нет Оценок!')
    else:
        text = 'Grades\n'
        for i in grade:
            text += f'Task: {find(i['id'])} | DATE: {i['submitted_at']} | Grade: {i['grade']}'
        await message.answer(green(text))



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
    await message.answer('Это бот HOMEWORK TRACKER\n\n/start - Для запуска бота\n/help - Для помощьи\n/show_users - Показать всех ползователей')

@router.message(F.text == 'PROFILE')
@router.message(Command('profile'))
async def profile(message: Message):
    user = message.from_user
    await message.answer(f'{user.full_name}\n\nID: {user.id} \nUsername: @{user.username}')

@router.message()
async def other(message: Message):
    user = message.from_user
    await message.answer(f'{user.username}: {message.text}\n\nBot: Можно по человечески')