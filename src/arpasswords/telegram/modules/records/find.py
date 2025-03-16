import os

import aiosqlite
from aiogram.types import Message

from . import show
from ... import base
from .... import database


@base.message(router=base.alt_router)
async def _command(message: Message) -> None:
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        labels: list[str] = [
            label
            for label in await database.labels(db)
            if message.text.lower() in label.lower()
        ]

    await show.records(message.from_user.id, labels)
