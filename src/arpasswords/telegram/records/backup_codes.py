import asyncio
import os

import aiosqlite
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message

from .. import base
from ... import database
from ...lang import _ as lang


@base.message(Command("backup_codes"))
async def _backup_codes(message: Message) -> None:
    label: str = message.text[message.text.find(" ") + 1:]
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        raw_backup_codes: list[str] | None = await database.parameter(db, message.from_user.id, label, "backup_codes")
        backup_codes: str = ""
        if raw_backup_codes is not None:
            for backup_code in raw_backup_codes:
                backup_codes += f"\n\t\t\t<code>{backup_code}</code>"
    parameter: str = (await lang("parameters", "backup_codes")).capitalize()
    text: str = (await lang("parameters", "show")).format(parameter=parameter, value=backup_codes)
    bot_message: Message = await message.answer(text)
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
