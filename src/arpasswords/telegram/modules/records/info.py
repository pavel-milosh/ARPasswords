import asyncio
import os
from typing import Any

import aiosqlite
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import  CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from ... import base
from .... import database
from ....config import _ as config
from ....lang import _ as lang


@base.router.callback_query(F.data.startswith("record_info"))
async def _callback_record_info(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    await record(callback.from_user.id, label)


async def record(user_id: int, label: str) -> None:
    parameters: dict[str, Any] = {}
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        for key in config()["parameters"]:
            if key not in ("label", "key"):
                parameters[key] = await database.parameter(db, user_id, label, key)
        parameters["label"] = label
    text: str = (await lang("records", "info")).format(**parameters)
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=await lang("otp", "get"), callback_data=f"otp {label}")],
        [InlineKeyboardButton(text=await lang("change", "parameter"), callback_data=f"change_parameter {label}")],
        [InlineKeyboardButton(text=await lang("records", "delete"), callback_data=f"sure_delete_record {label}")]
    ]

    bot_message: Message = await base.bot.send_message(
        user_id,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
