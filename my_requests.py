import aiohttp
import asyncio
import json

base_kompege_url = "https://kompege.ru/api/v1/task/{}"


async def get_task_by_kompege(task_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(base_kompege_url.format(task_id)) as response:
            return await response.json()


async def get_answer_by_kompege(task_id):
    task = await get_task_by_kompege(task_id)
    if task:
        return task["key"]
    return None
