import asyncio
import os
from typing import Any

import aiosqlite
import keyring
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import  CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from ... import _base
from .... import database
from ....config import _ as config
from ....local import _ as local


@_base.router.callback_query(F.data.startswith("record_info"))
async def _callback_record_info(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    await record(callback.from_user.id, label)


async def record(user_id: int, label: str) -> None:
    key_: str = await asyncio.to_thread(keyring.get_password,"keys", str(user_id))
    parameters: dict[str, Any] = {}
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        for key in config()["parameters"]:
            if key not in ("label", "key"):
                parameters[key] = await database.parameter(db, key_, label, key)
        parameters["label"] = label
    text: str = (await local("records", "info")).format(**parameters)
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=await local("records", "get_otp"), callback_data=f"otp {label}")],
        [InlineKeyboardButton(text=await local("change", "parameter"), callback_data=f"change_parameter {label}")],
        [InlineKeyboardButton(text=await local("records", "delete"), callback_data=f"sure_delete_record {label}")]
    ]

    bot_message: Message = await _base.bot.send_message(
        user_id,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
