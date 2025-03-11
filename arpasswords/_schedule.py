import asyncio
import os
import datetime

import keyring


async def _delete_keys() -> None:
    user_ids: list[str] = [
        user_id.replace(".db", "")
        for user_id in os.listdir("users")
    ]

    for user_id in user_ids:
        await asyncio.to_thread(keyring.delete_password, "keys", user_id)


async def _midnight() -> None:
    while True:
        now: datetime.datetime.now = datetime.datetime.now()
        midnight: datetime.datetime.combine = datetime.datetime.combine(
            now.date(),
            datetime.time(0, 0)
        )
        if now >= midnight:
            midnight = datetime.datetime.combine(
                now.date().replace(day=now.day + 1),
                datetime.time(0, 0)
            )

        seconds_until_midnight: float = (midnight - now).total_seconds()
        await asyncio.sleep(seconds_until_midnight)
        await _delete_keys()


async def setup() -> None:
    asyncio.create_task(_midnight())
