import os

import aiosqlite
from aiogram.types import Message

from . import _show
from ... import _base
from .... import database


@_base.message(router=_base.find_router)
async def _command(message: Message) -> None:
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        labels: list[str] = [
            label
            for label in await database.labels(db)
            if message.text.lower() in label.lower()
        ]

    await _show.records(message.from_user.id, labels)
