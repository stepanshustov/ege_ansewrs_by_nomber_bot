from aiogram import Bot, Dispatcher
from routers import app
import asyncio
import time
from config import *


# Создаем бота
async def start_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(app)
    await dp.start_polling(bot)


# Вечный цикл жизни бота, для выхода нажать Ctrl+C
if __name__ == "__main__":
    while True:
        try:
            asyncio.run(start_bot())
        except Exception as e:
            if e == KeyboardInterrupt:
                print("Bot stopped")
                exit(0)
            log_write(e)
            # raise e
        time.sleep(1)
