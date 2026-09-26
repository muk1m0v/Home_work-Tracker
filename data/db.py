from mukimov.color import green, red
from dotenv import load_dotenv
from os import getenv
import asyncpg

async def get_connection():
    try:
        conn = await asyncpg.connect(
            database=getenv
        )
        print(green('Tables Created!'))
    except Exception as err:
        print(red(f'Tables Created Error: {err}'))