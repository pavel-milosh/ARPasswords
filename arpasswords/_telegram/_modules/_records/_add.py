import os

import aiosqlite
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from . import _info
from ... import _base
from .... import _database
from ...._local import _ as _local


class AddRecord(StatesGroup):
    active: State = State()
    bot_message: Message


@_base.message(Command("add_record"))
async def _add_record(message: Message, state: FSMContext) -> None:
    await state.update_data(bot_message=await message.answer(await _local("records", "add")))
    await state.set_state(AddRecord.active)


@_base.message(AddRecord.active)
async def _add_record_active(message: Message, state: FSMContext) -> None:
    bot_message: Message = await state.get_value("bot_message")
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        await _database.add(db, message.text)
        await db.commit()
    await state.clear()
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
    await _info.record(message.from_user.id, message.text)
