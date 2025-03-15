import os

import aiosqlite
from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ... import base
from .... import database
from ....local import _ as local


@base.router.callback_query(F.data.startswith("sure_delete_record"))
async def _sure_delete_record(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    text: str = (await local("records", "sure_delete")).format(label=label)
    button: InlineKeyboardButton = InlineKeyboardButton(
        text=(await local("common", "yes")).capitalize(),
        callback_data=f"delete_record {label}"
    )
    await callback.message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[button]]))


@base.router.callback_query(F.data.startswith("delete_record"))
async def _delete_record(callback: CallbackQuery) -> None:
    await callback.answer()
    label: str = callback.data[callback.data.find(" ") + 1:]
    async with aiosqlite.connect(os.path.join("users", f"{callback.from_user.id}.db")) as db:
        await database.delete(db, label)
        await db.commit()
    await callback.message.edit_text((await local("records", "deleted")).format(label=label))
