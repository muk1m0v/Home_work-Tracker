from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from board import *
from service import *
from datetime import datetime

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
@router.message(Command('assignments'))
async def tasks(message: Message):
    user = message.from_user
    assignments = await get_assignments()
    sub = await get_all(user.id)
    if not assignments:
        await message.answer('У вас пока нет заданий!')
        return
    zhurnal = []
    for i in sub:
        zhurnal.append(i['assignment_id'])
    text = '📚 Ваши задания:\n\n'
    count = 0
    for task in assignments:
        if task['id'] not in zhurnal:
            text += (f"ID: {task['id']}\nTITLE: {task['title']}\nDATE AT: {task['due_date']}\n\n")
            count += 1
    if count == 0:
        await message.answer('Вы сдали все задания! ✅')
        return
    await message.answer(text)

@router.message(Command('add_assignment'))
async def add_assigment(message: Message, command: CommandObject):
    user = message.from_user
    if not command.args:
        await message.answer('Введите так!\n/add_assignment Сделать Database для проекта, 2026-10-02 (тут важена запитая , )')
        return
    add = command.args.split(',')
    if len(add) != 2:
        await message.answer('Введите 2 текста и всё пример после комманды\nЭкзамен, 2026-09-28')
        return
    title = add[0].strip()
    date_text = add[1].strip()
    if not title or not date_text:
        await message.answer('Введите 2 текста и всё пример после комманды\nЭкзамен, 2026-09-28')
        return
    try:
        due_date = datetime.strptime(date_text, '%Y-%m-%d').date()
    except Exception:
        await message.answer('Дата не такая! Надо так: 2026-09-28')
        return
    await add_assing(title, due_date)
    text = f'ВЫ {user.full_name}\nдобавили задание!✅\n\nTASK: {title}\n\nDATE: {date_text}'
    await message.answer(text)

@router.message(F.text == 'Выпольнить Задание')
async def sub_help(message: Message):
    await message.answer('Исползуй команду:\n/submit 1 - виполгить задание под ID: 1')

@router.message(F.text == 'Добавить Задание')
async def add_help(message: Message):
    await message.answer('Исползуй команду:\n/add_assignment Сделать экзамен, 2026-09-30 - Пример ввода!')

@router.message(F.text == 'Поставить оценку')
async def grade_help(message: Message):
    await message.answer('Исползуй команду:\n/set_grade 1, 95 - Пример ввода!')

@router.message(Command("submit"))
async def submit(message: Message, command: CommandObject):
    user = message.from_user
    sub = command.args
    if not sub:
        await message.answer('ID: НЕ МОЖЕТЬ БИТЬ ПУСТЫМ!')
        return
    sub = sub.strip()
    try:
        assignment_id = int(sub)
    except Exception:
        await message.answer('ID должен быть числом!\nПример: /submit 1')
        return
    completed = await new_submit(user.id, assignment_id)
    if completed == 'ok':
        await message.answer(f'Вы сдали задание: {assignment_id} ✅')
    elif completed == 'already':
        await message.answer(f'Вы уже сдавали задание: {assignment_id}')
    elif completed == 'no_assignment':
        await message.answer(f'У вас нет задачи с ID: {assignment_id}')
    else:
        await message.answer(f'У вас нет задачи с ID: {assignment_id}')

@router.message(Command('set_grade'))
async def set_grade(message: Message, command: CommandObject):
    if not command.args:
        await message.answer('Исползуй команду:\n/set_grade 1, 95 - Пример ввода!')
        return
    arg = command.args.split(',')
    if len(arg) != 2:
        await message.answer('Надо 2 числа через запятую!\nПример: /set_grade 1, 95')
        return
    try:
        assignment_id = int(arg[0].strip())
        grade = int(arg[1].strip())
    except Exception:
        await message.answer('ID и оценка должны быть числами!\nПример: /set_grade 1, 95')
        return
    if grade < 1 or grade > 100:
        await message.answer('Оценка от 1 до 100!')
        return
    res = await set_grade_db(message.from_user.id, assignment_id, grade)
    if res is None:
        await message.answer('У вас пока нет выполненных заданий с таким ID! Сначала /submit')
    else:
        await message.answer(f'✅ Оценка {grade} поставлена!')

@router.message(F.text == '📊 Мои оценки')
@router.message(Command('my_grades'))
async def grades(message: Message):
    user = message.from_user
    rows = await my_grades(user.id)
    if not rows:
        await message.answer('У вас пока нет оценок!')
        return
    text = '📊 Grades\n\n'
    for i in rows:
        grade_text = i['grade'] if i['grade'] is not None else 'без оценки'
        text += (f"Task: {i['title']}\nDATE: {i['submitted_at']}\nGrade: {grade_text}\n\n")
    await message.answer(text)

@router.message(F.text == 'Моя Сред.Оценка')
@router.message(Command('average_grade'))
async def average(message: Message):
    user = message.from_user
    avg = await avg_score(user.id)
    if avg is None:
        await message.answer('У вас пока нет оценок!')
        return
    await message.answer(f'📊 Ваш средний балл: {round(avg, 2)}')

@router.message(F.text == 'MENU')
@router.message(Command('menu'))
async def start_menu(message: Message):
    await message.answer('Привет это меню для Проверки домашных заданый!\n\n/assignments - показать все мои задание\n/add_assignment - Добавить задание\n/submit - Выполнить звдание\n/set_grade - Поставить оценку\n/my_grades - Показать все мои оценки\n/average_grade - Средный балл по всех заланиям!', reply_markup=menu())

@router.message(F.text == 'SHOW ALL USERS')
@router.message(Command('show_users'))
async def other_users(message: Message):
    users = await get_users()
    if not users:
        await message.answer('Пока нет пользователей!')
    else:
        text = 'Users:\n'
        for i in users:
            text += f"ID: {i['id']} | Username: @{i['username']} | {i['full_name']}\n"
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
