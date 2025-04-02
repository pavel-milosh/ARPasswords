import asyncio
import logging
import os

import aiosqlite
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from pyotp import TOTP

from .. import base
from ... import database, logger
from ...lang import _ as lang


def _get_totp_code(totp: str) -> str:
    return TOTP(totp).now()


@base.message(Command("totp"))
async def _totp(message: Message) -> None:
    label: str = message.text[message.text.find(" ") + 1:]
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        totp: str = f"<code>{await database.parameter(db, message.from_user.id, label, 'totp')}</code>"
    parameter: str = (await lang("parameters", "totp")).capitalize()
    text: str = (await lang("parameters", "show")).format(parameter=parameter, value=totp)
    bot_message: Message = await message.answer(text)
    await logger.user(logging.INFO, message.from_user.id, "totp_viewed", label=label)
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass


@base.router.callback_query(F.data.startswith("totp_code"))
async def _totp_code(callback: CallbackQuery) -> None:
    label: str = callback.data[callback.data.find(" ") + 1:]
    async with aiosqlite.connect(os.path.join("users", f"{callback.from_user.id}.db")) as db:
        totp: str = await database.parameter(db, callback.from_user.id, label, "totp")
    totp_code: str = await asyncio.to_thread(_get_totp_code, totp)
    text: str = (await lang("records", "totp_code_message")).format(totp_code=totp_code)
    message: Message = await callback.message.answer(text)
    await logger.user(logging.INFO, message.from_user.id, "totp_code_viewed", label=label)
    await callback.answer(await lang("records", "totp_code_callback"))
    await asyncio.sleep(30)
    await message.delete()
