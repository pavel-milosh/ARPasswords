import asyncio
import logging
import os

import aiosqlite
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message

from .. import base
from ... import database, logger
from ...lang import _ as lang


@base.message(Command("note"))
async def _note(message: Message) -> None:
    label: str = message.text[message.text.find(" ") + 1:]
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        raw_note: str | None = await database.parameter(db, message.from_user.id, label, "note")
    note: str = f"\n<code>{str(raw_note)}</code>"
    parameter: str = (await lang("parameters", "note")).capitalize()
    text: str = (await lang("parameters", "show")).format(parameter=parameter, value=note)
    bot_message: Message = await message.answer(text)
    await logger.user(logging.INFO, message.from_user.id, "note_viewed", label=label)
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
