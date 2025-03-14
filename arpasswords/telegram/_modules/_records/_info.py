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
    label: str = callback.data[callback.data.find(" ") + 1:]
    await callback.message.delete()
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
        [InlineKeyboardButton(text=await local("records", "get_otp"), callback_data=f"otp {label}")]
    ]
    for key in config()["parameters"]:
        if key not in ("label", "key"):
            value: str = await local("parameters", key)
            button_text: str = (await local("common", "change_?")).format(parameter=value)
            callback_data: str = f"change_{key} {label}"
            buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])

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
