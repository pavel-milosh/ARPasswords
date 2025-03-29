import asyncio
import os
from datetime import datetime, time

import keyring


async def _delete_keys() -> None:
    user_ids: list[str] = [user_id.replace(".db", "") for user_id in os.listdir("users")]
    for user_id in user_ids:
        try:
            await asyncio.to_thread(keyring.delete_password, "keys", user_id)
        except:
            pass


async def _midnight() -> None:
    while True:
        now: datetime.now = datetime.now()
        midnight: datetime.combine = datetime.combine(now.date(), time(0, 0))
        if now >= midnight:
            midnight = datetime.combine(now.date().replace(day=now.day + 1), time(0, 0))
        seconds_until_midnight: float = (midnight - now).total_seconds()
        await asyncio.sleep(seconds_until_midnight)
        asyncio.create_task(_delete_keys())


async def setup() -> None:
    asyncio.create_task(_midnight())
