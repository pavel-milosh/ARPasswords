import os

import keyring
import aiosqlite
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from . import _info
from ... import _base, _decorators
from .... import database
from ....local import _ as local


class ChangeFields(StatesGroup):
    active: State = State()
    parameter: str
    label: str
    bot_message: Message


@_base.dp.callback_query(F.data.startswith("change_"))
async def _change(callback: CallbackQuery, state: FSMContext) -> None:
    parameter: str = callback.data.split()[0].replace("change_", "")
    await state.set_state(ChangeFields.active)
    await state.update_data(
        parameter=parameter,
        label=callback.data.split()[1]
    )
    await callback.message.delete()
    await state.update_data(
        bot_message=await callback.message.answer(
            local("records", "enter_new_?").format(
                parameter=local("parameters", parameter).capitalize()
            )
        )
    )
    await callback.answer()

@_base.dp.message(ChangeFields.active)
@_decorators.messages_controller()
async def _change_active(message: Message, state: FSMContext) -> None:
    key: str = keyring.get_password("keys", str(message.from_user.id))
    parameter: str = await state.get_value("parameter")
    label: str = await state.get_value("label")
    bot_message: Message = await state.get_value("bot_message")
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        await database.records.parameter(db, parameter, key, label, message.text)
        await db.commit()
    await bot_message.delete()
    await _info.record(message.from_user.id, label)
    await state.clear()