import os

import aiosqlite
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

from . import _info
from ... import _base
from .... import database
from ....local import _ as local


@_base.message(Command("show_records"))
async def _command_show_records(message: Message) -> None:
    await records(message.from_user.id)


async def records(user_id: int) -> None:
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        labels: list[str] = await database.labels(db)
    if len(labels) == 0:
        await _base.bot.send_message(user_id, local("records", "no_records_found"))
    elif len(labels) == 1:
        await _info.record(user_id, labels[0])
    else:
        buttons: list[list[InlineKeyboardButton]] = [
            [InlineKeyboardButton(text=label, callback_data=f"record_info {label}")]
            for label in labels
        ]
        await _base.bot.send_message(
            user_id,
            local("records", "choose_record"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )