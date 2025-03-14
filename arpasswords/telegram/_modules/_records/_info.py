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
from ....local import _ as local


@_base.router.callback_query(F.data.startswith("record_info"))
async def _callback_record_info(callback: CallbackQuery) -> None:
    label: str = callback.data[callback.data.find(" ") + 1:]
    await callback.message.delete()
    await record(callback.from_user.id, label)


async def record(user_id: int, label: str) -> None:
    key: str = await asyncio.to_thread(keyring.get_password,"keys", str(user_id))
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        data: dict[str, Any] = {
            key_: await database.parameter(db, key, label, key_)
            for key_ in dict((await local("parameters"))._catalog)
            if key_ not in ("", "label", "key")
        }

    data["label"] = label
    text: str = (await local("records", "info")).format(**data)
    bot_message: Message = await _base.bot.send_message(user_id, ".")
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=await local("records", "get_otp"), callback_data=f"otp {label}")]
    ]
    for key, value in dict((await local("parameters"))._catalog).items():
        if key not in ("", "label", "key"):
            button_text: str = (await local("common", "change_?")).format(parameter=value)
            callback_data: str = f"change_{key} {label}"
            buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])

    await bot_message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
