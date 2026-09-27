from services.db import get_connection
from mukimov.color import green, red


async def get_users():
    conn = None
    try:
        conn = await get_connection()
        get_user = await conn.fetch('''
        SELECT * FROM users
        ''')
        return get_user
    except Exception as err:
        print(red(f'Get Users Error: {err}'))
        return []
    finally:
        if conn:
            await conn.close()

async def get_assignments():
    conn = None
    try:
        conn = await get_connection()
        return await conn.fetch(
            'SELECT * FROM assignments ORDER BY id'
        )
    except Exception as err:
        print(red(f'Get Assignments Error: {err}'))
        return []
    finally:
        if conn:
            await conn.close()

async def get_all(telegram_id):
    conn = None
    try:
        conn = await get_connection()
        tasker = await conn.fetch('''
            SELECT s.assignment_id FROM submissions as s
            INNER JOIN users as u ON s.user_id = u.id
            WHERE u.telegram_id = $1
            ''', str(telegram_id))
        return tasker
    except Exception as err:
        print(red(f'Get All Error: {err}'))
        return []
    finally:
        if conn:
            await conn.close()

async def found_task(assignment_id):
    conn = None
    try:
        conn = await get_connection()
        find_task = await conn.fetchval('''
        SELECT title from assignments where id = $1
        ''', int(assignment_id))
        return find_task
    except Exception as err:
        print(red(f'Found Task Error: {err}'))
        return None
    finally:
        if conn:
            await conn.close()

async def check_users(telegram_id):
    conn = None
    try:
        conn = await get_connection()
        check_user = await conn.fetch('''
        SELECT * FROM users where telegram_id = $1
        ''', str(telegram_id))
        return check_user
    except Exception as err:
        print(red(f'Check Users Error: {err}'))
        return []
    finally:
        if conn:
            await conn.close()

async def save_user(telegram_id, username, full_name):
    conn = None
    try:
        conn = await get_connection()
        await conn.execute('''
        INSERT INTO users (telegram_id, username, full_name) VALUES
        ($1, $2, $3)
        ''', str(telegram_id), username, full_name)
    except Exception as err:
        print(red(f'Add Users Error: {err}'))
    finally:
        if conn:
            await conn.close()

async def add_assing(title, date):
    conn = None
    try:
        conn = await get_connection()
        await conn.execute('''
        INSERT INTO assignments (title, due_date) VALUES
        ($1,$2)
        ''', title, date)
    except Exception as err:
        print(red(f'Add Assignment Error: {err}'))
    finally:
        if conn:
            await conn.close()

async def set_grade_db(telegram_id, assignment_id, grade):
    conn = None
    try:
        conn = await get_connection()
        res = await conn.fetchval('''
        UPDATE submissions as s SET grade = $1
        FROM users as u
        WHERE s.user_id = u.id
        AND u.telegram_id = $2
        AND s.assignment_id = $3
        RETURNING s.id
        ''', int(grade), str(telegram_id), int(assignment_id))
        return res
    except Exception as err:
        print(red(f'Set Grade Error: {err}'))
        return None
    finally:
        if conn:
            await conn.close()

async def new_submit(telegram_id, assignment_id):
    conn = None
    try:
        conn = await get_connection()
        user_id = await conn.fetchval('SELECT id FROM users WHERE telegram_id = $1',
        str(telegram_id))
        if user_id is None:
            return None
        task = await conn.fetchval('SELECT id FROM assignments WHERE id = $1',
        int(assignment_id))
        if task is None:
            return 'no_assignment'
        old = await conn.fetchval('''
        SELECT id FROM submissions WHERE user_id = $1 AND assignment_id = $2
        ''', user_id, int(assignment_id))
        if old is not None:
            return 'already'
        await conn.execute('''
        INSERT INTO submissions (user_id, assignment_id)
        VALUES ($1, $2)
        ''', user_id, int(assignment_id))
        return 'ok'
    except Exception as err:
        print(red(f'Add submissions Error: {err}'))
        return None
    finally:
        if conn:
            await conn.close()

async def my_grades(telegram_id):
    conn = None
    try:
        conn = await get_connection()
        rows = await conn.fetch('''
        SELECT s.assignment_id, s.submitted_at, s.grade, a.title FROM submissions as s
        JOIN users as u ON s.user_id = u.id
        JOIN assignments as a ON s.assignment_id = a.id
        WHERE u.telegram_id = $1
        ORDER BY s.assignment_id
        ''', str(telegram_id))
        return rows
    except Exception as err:
        print(red(f'My Grades Error: {err}'))
        return []
    finally:
        if conn:
            await conn.close()

async def avg_score(telegram_id):
    conn = None
    try:
        conn = await get_connection()
        avg = await conn.fetchval('''
        SELECT AVG(s.grade)::FLOAT FROM submissions as s
        JOIN users as u ON s.user_id = u.id
        WHERE u.telegram_id = $1 AND s.grade IS NOT NULL
        ''', str(telegram_id))
        return avg
    except Exception as err:
        print(red(f'Avg Score Error: {err}'))
        return None
    finally:
        if conn:
            await conn.close()
