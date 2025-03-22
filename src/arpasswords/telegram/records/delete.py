import os

import aiosqlite
from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from .. import base
from ... import database
from ...lang import _ as lang


@base.router.callback_query(F.data.startswith("delete_record"))
async def _delete_record(callback: CallbackQuery) -> None:
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    text: str = (await lang("records", "sure_delete")).format(label=label)
    button: InlineKeyboardButton = InlineKeyboardButton(
        text=(await lang("common", "yes")).capitalize(),
        callback_data=f"sure_delete_record {label}"
    )
    await callback.message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[button]]))
    await callback.answer(await lang("common", "request_operated"))


@base.router.callback_query(F.data.startswith("sure_delete_record"))
async def _sure_delete_record(callback: CallbackQuery) -> None:
    label: str = callback.data[callback.data.find(" ") + 1:]
    text: str = (await lang("records", "deleted")).format(label=label)
    async with aiosqlite.connect(os.path.join("users", f"{callback.from_user.id}.db")) as db:
        await database.delete(db, label)
        await db.commit()
    await callback.message.edit_text(text)
    await callback.answer(text)
