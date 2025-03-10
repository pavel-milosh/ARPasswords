import os

import keyring
import aiosqlite
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

from . import _info
from ... import _base, _decorators
from .... import database
from ....local import _ as local


# @_base.router.message()
@_decorators.messages_controller()
async def _find(message: Message) -> None:
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        labels: list[str] = [
            label
            for label in await database.records.labels()
            if message.text.lower() in label
        ]

    if len(labels) == 0:
        await message.answer(local("records", "no_records_found").format(query=message.text))
    elif len(labels) == 1:
        await _info.record(message.from_user.id, labels[0])
    else:
        buttons: list[list[InlineKeyboardButton]] = [
            [InlineKeyboardButton(text=label, callback_data=f"record_info {label}")]
            for label in labels
        ]
        await message.answer(
            local("records", "several_records_found"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )