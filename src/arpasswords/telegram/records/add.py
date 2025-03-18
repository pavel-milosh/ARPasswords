import os

import aiosqlite
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from . import info
from .. import base, cancel
from ... import database
from ...database.exceptions import LabelNotUnique
from ...lang import _ as lang


class AddRecord(StatesGroup):
    active: State = State()
    bot_message: Message


@base.message(Command("add_record"))
async def _add_record(message: Message, state: FSMContext) -> None:
    bot_message: Message = await message.answer(
        await lang("records", "add"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[await cancel.button()]])
    )
    await state.update_data(bot_message=bot_message)
    await state.set_state(AddRecord.active)


@base.message(AddRecord.active)
async def _add_record_active(message: Message, state: FSMContext) -> None:
    bot_message: Message = await state.get_value("bot_message")
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        try:
            await database.add(db, message.text)
        except LabelNotUnique:
            keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[await cancel.button()]])
            await bot_message.edit_text(await lang("common", "incorrect_value"), reply_markup=keyboard)
            return
        await db.commit()
    await state.clear()
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
    await info.record(message.from_user.id, message.text)
