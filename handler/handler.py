from aiogram import Router, F 
from aiogram.filters import CommandStart, Command, CommandObject 
from aiogram.types import Message
from board import *
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

@router.message(F.text == '📚 Задания')
@router.message(Command('assigments'))
async def tasks(message: Message):
    user = message.from_user
    assignments = await get_assignments()
    sub = await get_all(user.id)
    zhurnal = []

    if not sub:
        await message.answer('У вас пока нет заданый!')
        return

    for i in sub:
        zhurnal.append(i['assignment_id'])
        

    text = '📚 Ваши задания:\n\n'
    for task in assignments:
        if task['id'] not in zhurnal:
            text += (
                f"ID: {task['id']}\n"
                f"TITLE {task['title']}\n"
                f"DATE AT: {task['due_date']}\n\n"
            )

    await message.answer(text)



@router.message(Command('add_assigment'))
async def add_assigment(message: Message, command: CommandObject):
    user = message.from_user
    add = command.args.split(',')
    if not add:
        await message.answer('Введите так!\n/add_assigment Сделать Database для проекта, 2026-10-02 (тут важена запитая , )')
    elif len(add) > 2:
        await message.answer('Введите 2 текста и всё пример после коммандыn\nЭкзамен, 2026-09-28')
    else:
        await add_assing(add[0], add[1])
        text = f'ВЫ {user.full_name}\nдобавили задание\n\nTASK: {add[0]}\n\nDATE: {add[1]}'
        await message.answer(text)

@router.message(F.text == 'Выпольнить Задание')
async def sub_it(message: Message):
    await message.answer('Исползуй команду:\n/submit 1 - виполгить задание под ID: 1')

@router.message(F.text == 'Добавить Задание')
async def sub_it(message: Message):
    await message.answer('Исползуй команду:\n/add_assigment Сделать экзамен, 2026-09-30 - Пример ввода!')

@router.message(F.text == 'Поставить оценку')
async def sub_it(message: Message):
    await message.answer('Исползуй команду:\n/set_grade Сделать экзамен, 2026-090-30 - Пример ввода!')

@router.message(Command("submit"))
async def submit(message: Message, command: CommandObject):
    user = message.from_user
    sub = command.args
    completed = await new_submit(user.id, sub)
    if not completed:
        await message.answer(F'У вас нет задачи с ID: {sub}')
    else:
        await message.answer(f'Вы сдали задани: {sub}')

@router.message(F.text == '📊 Мои оценки')
@router.message(Command('my_grade'))
async def grades(message: Message):
    user = message.from_user
    grade = await my_grades(user.id)
    if not grade:
        await message.answer('У вас пока нет Оценок!')
    else:
        text = 'Grades\n'
        for i in grade:
            text += f'Task: {found_task(i['id'])} | DATE: {i['submitted_at']} | Grade: {i['grade']}'
        await message.answer(green(text))

@router.message(F.text == 'MENU')
@router.message(Command('menu'))
async def start_menu(message: Message):
    await message.answer('Привет это меню для Проверки домашных заданый!\n\n/assigments - показать все мои задание\n/add_assigment - Добавить задание\n/submit - Выполнить звдание\n/set_grade - Поставить оценку\n/my_grades - Показать все мои оценки\n/average_grade - Средный балл по всех заланиям!', reply_markup=menu())

@router.message(F.text == 'SHOW ALL USERS')
@router.message(Command('show_users'))
async def other(message: Message):
    users = await get_users()
    if not users:
            await message.answer('Пока нет пользователей!')
    else:
        text = 'Users:\n'
        for i in users:
            text += f'ID: {i['id']} | Username: @{i['username']} | {i['full_name']}'
        await message.answer(text)

@router.message(F.text == 'HELP')
@router.message(Command('help'))
async def help(message: Message):
    await message.answer('Это бот HOMEWORK TRACKER\n\n/start - Для запуска бота\n/help - Для помощьи\n/show_users - Показать всех ползователей\n/menu - Меню для проверки заданый')

@router.message(F.text == 'PROFILE')
@router.message(Command('profile'))
async def profile(message: Message):
    user = message.from_user
    await message.answer(f'{user.full_name}\n\nID: {user.id} \nUsername: @{user.username}')

@router.message()
async def other(message: Message):
    user = message.from_user
    await message.answer(f'@{user.username}: {message.text}\n\nBot: Можно по человечески')