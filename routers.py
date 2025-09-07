import time
from typing import *
from aiogram.filters import *
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, BaseMiddleware
from aiogram.types import *

from my_requests import get_answer_by_kompege
from config import *

# защита от спама
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.last_processed = {}

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Проверяем, что событие - это сообщение
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        current_time = time.time()

        # Проверяем время последнего сообщения
        if user_id in self.last_processed:
            elapsed = current_time - self.last_processed[user_id]
            if elapsed < self.rate_limit:
                # Если сообщение пришло слишком рано - блокируем
                await event.answer("⏳ Слишком часто! Подождите немного...")

        # Обновляем время последнего сообщения
        self.last_processed[user_id] = current_time
        return await handler(event, data)


class MyStates(StatesGroup):
    users_request = State()


app = Router()
app.message.middleware(ThrottlingMiddleware(5))  # запрос раз в 5 секунд


@app.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(START_MESSAGE, parse_mode="html", )


@app.message(Command("help"))
async def help_(message: Message):
    await message.answer(HELP_MESSAGE, parse_mode="html")


@app.message()
async def users_request(message: Message, state: FSMContext):
    t = message.text.strip()
    if not t.strip().replace(' ', '').isnumeric():
        await message.answer("Номер должен состоять из цифр!")
        return
    ans = await get_answer_by_kompege(t)
    if ans is None:
        await message.answer(
            "❌ Не удалось найти ответ по вашему запросу!",
            parse_mode="html"
        )
        return
    await message.answer(f"Ответ: <b>{ans}</b>", parse_mode="html")
