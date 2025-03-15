import os

import aiosqlite
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from . import info
from ... import base
from .... import database
from ....local import _ as local


@base.message(Command("show_records"))
async def _command_show_records(message: Message) -> None:
    await records(message.from_user.id)


async def records(user_id: int, labels: list[str] | None = None) -> None:
    if labels is None:
        async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
            labels: list[str] = await database.labels(db)

    if len(labels) == 0:
        await base.bot.send_message(user_id, await local("records", "not_found"))
    elif len(labels) == 1:
        await info.record(user_id, labels[0])
    else:
        buttons: list[list[InlineKeyboardButton]] = [
            [InlineKeyboardButton(text=label, callback_data=f"record_info {label}")]
            for label in labels
        ]
        keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await base.bot.send_message(user_id, await local("records", "choose"), reply_markup=keyboard)
