from data.db import get_connection
from mukimov.color import green, red


async def get_users():
    try:
        conn = await get_connection()
        get_user = await conn.fetch('''
        SELECT * FROM users
        ''') 
        
        print(green('Users Get'))
        return get_user
    except Exception as err:
        print(red(f'Get Users Error: {err}'))
    finally:
        await conn.close()

