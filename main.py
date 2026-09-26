from aiogram import Dispatcher, Bot
from mukimov.color import green
from data.db import init_tables
from handler.handler import router
from os import getenv
from dotenv import load_dotenv
import asyncio

load_dotenv()

bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher()


async def main():
    print(green('Bot Started!'))

    dp.include_router(router)
    await init_tables()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())