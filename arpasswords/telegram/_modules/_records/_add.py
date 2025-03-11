import os

import aiosqlite
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from . import _info
from ... import _base
from .... import database
from ....local import _ as local


class AddRecord(StatesGroup):
    label_state: State = State()
    password_state: State = State()
    label: str
    password: str
    url: str = None
    totp: str = None
    backup_codes: list[str] | None = None
    bot_message: Message
    user_message: Message


@_base.message(Command("add_record"))
async def _add_record(message: Message, state: FSMContext) -> None:
    await state.set_state(AddRecord.label_state)
    await state.update_data(
        bot_message=await message.answer(local("c_add_record", "initial")),
    )


@_base.message(AddRecord.label_state)
async def _add_record_label(message: Message, state: FSMContext) -> None:
    await state.set_state(AddRecord.password_state)
    await state.update_data(label=message.text)
    bot_message: Message = await state.get_value("bot_message")
    await bot_message.edit_text(local("c_add_record", "enter_password"))


@_base.message(AddRecord.password_state, get_parameters=("key",))
async def _add_record_password(message: Message, state: FSMContext, **kwargs) -> None:
    await state.update_data(password=message.text)
    label: str = await state.get_value("label")
    password: str = await state.get_value("password")
    bot_message: Message = await state.get_value("bot_message")
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        await database.add(db, kwargs["key"], label, password)
        await db.commit()
    await bot_message.delete()
    await _info.record(message.from_user.id, label)
    await state.clear()
