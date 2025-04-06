import asyncio
import logging
import os

import aiofiles
import aiofiles.os

from . import keys, logger


async def _delete() -> None:
    user_ids: list[str] = [
        user_id.replace(".db", "")
        for user_id in os.listdir("users")
        if user_id.endswith(".db")
    ]
    await keys._.reencrypt()
    for user_id in user_ids:
        path: str = os.path.join("users", f"{user_id}.log")
        try:
            if await aiofiles.os.path.exists(path):
                async with aiofiles.open(path, "w") as file:
                    await file.write("")
        except:
            pass
        await logger.user(logging.INFO, int(user_id), "schedule")


async def _24_hours() -> None:
    while True:
        asyncio.create_task(_delete())
        await asyncio.sleep(24 * 60 * 60)


async def setup() -> None:
    asyncio.create_task(_24_hours())
