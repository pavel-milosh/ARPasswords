import asyncio
import os

import aiosqlite
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from .. import base
from ... import database
from ...config import _ as config
from ...lang import _ as lang


@base.router.callback_query(F.data.startswith("record_info"))
async def _record_info(callback: CallbackQuery) -> None:
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    await callback.answer(await lang("common", "request_operated"))
    await record(callback.from_user.id, label)


async def record(user_id: int, label: str) -> None:
    text: str = ""
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        for parameter in config()["parameters"] + await database.additional_parameters(db, user_id, label):
            name: str = (await lang("parameters", parameter)).capitalize()
            if parameter == "label":
                continue
            if parameter in ("totp", "backup_codes", "note"):
                text += f"\n\t\t\t\t\t<b>{name}:</b>  <code>/{parameter} {label}</code>"
            else:
                value: str | None = await database.parameter(db, user_id, label, parameter)
                text += f"\n\t\t\t\t\t<b>{name}:</b>  <code>{value}</code>"
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=await lang("records", "totp_code_button"), callback_data=f"totp_code {label}")],
        [InlineKeyboardButton(text=await lang("edit", "parameter"), callback_data=f"edit_parameter {label}")],
        [InlineKeyboardButton(text=await lang("records", "add_parameter"), callback_data=f"add_parameter {label}")],
        [InlineKeyboardButton(text=await lang("records", "delete"), callback_data=f"delete_record {label}")]
    ]
    bot_message: Message = await base.bot.send_message(
        user_id,
        (await lang("records", "info")).format(label=label, info=text),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
