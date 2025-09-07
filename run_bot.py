from aiogram import Bot, Dispatcher
from routers import app
import asyncio

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# get token from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")


# function to start bot
async def start_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot=bot)
    dp.include_router(app)
    await dp.start_polling()


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(start_bot())
        except Exception as e:
            if e == KeyboardInterrupt:
                print("Bot stopped")
                exit(0)
            with open("logs.txt", "a") as f:
                print(f"---\n{datetime.now()}\nError: {e}\n---", file=f)
