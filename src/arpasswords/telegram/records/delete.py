import logging
import os

import aiosqlite
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from .. import base
from ... import database, logger
from ...keys import _ as keys
from ...lang import _ as lang


class DeleteAll(StatesGroup):
    active: State = State()
    bot_message: Message


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
        await database.delete(db, callback.from_user.id, label)
        await db.commit()
    await callback.message.edit_text(text)
    await callback.answer(text)


@base.message(Command("delete_all"), ignore_key=True)
async def _delete_all(message: Message, state: FSMContext) -> None:
    text: str = (await lang("commands", "delete_all_message")).format(user_id=message.from_user.id)
    await state.update_data(bot_message=await message.answer(text))
    await state.set_state(DeleteAll.active)


@base.message(DeleteAll.active, ignore_key=True)
async def _delete_all_active(message: Message, state: FSMContext) -> None:
    bot_message: Message = await state.get_value("bot_message")
    await state.clear()
    if message.text == f"delete_all {message.from_user.id}":
        os.remove(os.path.join("users", f"{message.from_user.id}.db"))
        try:
            keys.delete(message.from_user.id)
        except KeyError:
            pass
        await bot_message.edit_text(await lang("commands", "delete_all_deleted"))
        await logger.user(logging.INFO, message.from_user.id, "deleted_all")
    else:
        await bot_message.edit_text(await lang("commands", "delete_all_not_deleted"))
