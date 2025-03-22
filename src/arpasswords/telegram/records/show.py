import math
import os
from typing import Any

import aiosqlite
from aiogram import F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from . import info
from .. import base
from ... import database
from ...lang import _ as lang


@base.message(router=base.alt_router)
async def _find(message: Message) -> None:
    await records(message, True)

@base.message(Command("show_records"))
async def _show_records(message: Message) -> None:
    await records(message, False)

@base.router.callback_query(F.data.startswith("forward"))
async def _forward(callback: CallbackQuery) -> None:
    await callback.answer()
    data_str: str = callback.data.replace("forward ", "")
    data: dict[str, Any] = {
        "user_id": int(data_str.split("|")[0]),
        "message_id": int(data_str.split("|")[1]),
        "current_page": int(data_str.split("|")[2]) + 1,
        "message_text": None if data_str.split("|")[3] == "None" else data_str.split("|")[3]
    }
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=await _buttons(data))
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@base.router.callback_query(F.data.startswith("back"))
async def _back(callback: CallbackQuery) -> None:
    await callback.answer()
    data_str: str = callback.data.replace("back ", "")
    data: dict[str, Any] = {
        "user_id": int(data_str.split("|")[0]),
        "message_id": int(data_str.split("|")[1]),
        "current_page": int(data_str.split("|")[2]) - 1,
        "message_text": None if data_str.split("|")[3] == "None" else data_str.split("|")[3]
    }
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=await _buttons(data))
    await callback.message.edit_reply_markup(reply_markup=keyboard)


async def _buttons(data: dict[str, Any]) -> list[list[InlineKeyboardButton]]:
    async with aiosqlite.connect(os.path.join("users", f"{data['user_id']}.db")) as db:
        if data["message_text"] is not None:
            labels: list[str] = [label for label in await database.labels(db) if data["message_text"].lower() in label.lower()]
        else:
            labels: list[str] = await database.labels(db)

    pages: int = math.ceil(len(labels) / 10)
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=label, callback_data=f"record_info {label}")]
        for label in sorted(labels)
    ]
    if pages > 1:
        buttons = buttons[10 * (data["current_page"] - 1):10 * data["current_page"]]
        data_str: str = "|".join([str(value) for value in data.values()])
        if data["current_page"] != 1:
            buttons.append([InlineKeyboardButton(text="<<<", callback_data=f"back " + data_str)])
        if data["current_page"] < pages:
            buttons.append([InlineKeyboardButton(text=">>>", callback_data=f"forward " + data_str)])
    return buttons



async def records(message: Message, find: bool) -> None:
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        if find:
            labels: list[str] = [label for label in await database.labels(db) if message.text.lower() in label.lower()]
        else:
            labels: list[str] = await database.labels(db)

    if len(labels) == 0:
        await base.bot.send_message(message.from_user.id, await lang("records", "not_found"))
    elif len(labels) == 1:
        await info.record(message.from_user.id, labels[0])
    else:
        bot_message: Message = await base.bot.send_message(message.from_user.id, await lang("records", "choose"))
        data: dict[str, Any] = {
            "user_id": message.from_user.id,
            "message_id": message.message_id,
            "current_page": 1,
            "message_text": None
        }
        keyboard: InlineKeyboardMarkup
        if find:
            data["message_text"] = message.text
        keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=await _buttons(data))
        await bot_message.edit_reply_markup(reply_markup=keyboard)
