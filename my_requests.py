import aiohttp
import asyncio
import json

from config import log_write

base_kompege_url = "https://kompege.ru/api/v1/task/{}"


async def get_task_by_kompege(task_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(base_kompege_url.format(task_id)) as response:
            if response.status != 200:
                log_write(response.status)
                return None
            return await response.json()


async def get_answer_by_kompege(task_id):
    task = await get_task_by_kompege(task_id)
    if task is not None:
        return task["key"]
    return None
