import os

import aiosqlite
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from . import _info
from ... import _base
from .... import database
from ....local import _ as local


class AddRecord(StatesGroup):
    active: State = State()
    bot_message: Message


@_base.message(Command("add_record"))
async def _add_record(message: Message, state: FSMContext) -> None:
    await state.update_data(bot_message=await message.answer(await local("records", "add")))
    await state.set_state(AddRecord.active)


@_base.message(AddRecord.active)
async def _add_record_label(message: Message, state: FSMContext) -> None:
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        await database.add(db, message.text)
        await db.commit()

    bot_message: Message = await state.get_value("bot_message")
    await bot_message.delete()
    await _info.record(message.from_user.id, message.text)
    await state.clear()
