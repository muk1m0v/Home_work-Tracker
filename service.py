from data.db import get_connection
from mukimov.color import green, red


async def get_users():
    try:
        conn = await get_connection()
        get_user = await conn.fetch('''
        SELECT * FROM users
        ''') 

        return get_user
    except Exception as err:
        print(red(f'Get Users Error: {err}'))
    finally:
        await conn.close()

async def found_task(assignment_id):
    try:
        conn = await get_connection()
        find_user = await conn.fetch('''
        SELECT title from assignments where id = $1
        ''', assignment_id) 

        return find_user
    except Exception as err:
        print(red(f'Found User Error: {err}'))
    finally:
        await conn.close()

async def check_users(telegram_id):
    try:
        conn = await get_connection()
        check_user = await conn.fetch('''
        SELECT * FROM users where telegram_id = $1
        ''', str(telegram_id)) 

        return check_user
    except Exception as err:
        print(red(f'Check Users Error: {err}'))
    finally:
        await conn.close()

async def save_user(telegram_id, username, full_name):
    try:
        conn = await get_connection()
        await conn.execute('''
        INSERT INTO users (telegram_id, username, full_name) VALUES
        ($1, $2, $3)
        ''', str(telegram_id), username, full_name) 
    except Exception as err:
        print(red(f'Add Users Error: {err}'))
    finally:
        await conn.close()


async def new_submit(user_id, assignment_id):
    try:
        conn = await get_connection()
        await conn.execute('''
        INSERT INTO submissions (user_id, assignment_id) VALUES 
        ($1, $2);
        ''', str(user_id), assignment_id) 
    except Exception as err:
        print(red(f'Add submissions Error: {err}'))
    finally:
        await conn.close()

async def my_grades(telegram_id):
    try:
        conn = await get_connection()
        await conn.fetch('''
        SELECT s.* FROM submissions as s
        JOIN users as u ON s.user_id = u.id
        WHERE u.telegram_id = $1;
        ''', str(telegram_id))
    except Exception as err:
        print(red(f'Add Grades Error: {err}'))
    finally:
        await conn.close()