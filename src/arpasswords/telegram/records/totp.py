import asyncio
import os

import aiosqlite
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message

from .. import base
from ... import database
from ...lang import _ as lang


@base.message(Command("totp"))
async def _totp(message: Message) -> None:
    label: str = message.text[message.text.find(" ") + 1:]
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        totp: str = f"<code>{await database.parameter(db, message.from_user.id, label, 'totp')}</code>"
    parameter: str = (await lang("parameters", "totp")).capitalize()
    text: str = (await lang("parameters", "show")).format(parameter=parameter, value=totp)
    bot_message: Message = await message.answer(text)
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
