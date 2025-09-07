from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Получаем токен из файла .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

START_MESSAGE = """Привет, я помогу тебе быстро узнать ответ с сайта КомпЕГЭ
Просто введи номер задания
Ограничения: <b> 1 запрос в 5 секунд </b>"""

HELP_MESSAGE = START_MESSAGE
