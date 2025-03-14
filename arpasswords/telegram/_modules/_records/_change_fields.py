import os

import aiosqlite
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from . import _info
from .. import _cancel
from ... import _base
from .... import database
from ....local import _ as local


class ChangeFields(StatesGroup):
    active: State = State()
    bot_message: Message
    label: str
    parameter: str


@_base.alt_router.callback_query(F.data.startswith("change_"))
async def _change(callback: CallbackQuery, state: FSMContext) -> None:
    label: str = callback.data[callback.data.find(" ") + 1:]
    parameter: str = callback.data.split()[0].replace("change_", "")
    parameter_text: str = (await local("parameters", parameter)).capitalize()
    text: str = (await local("common", "enter_new_?")).format(parameter=parameter_text)
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[await _cancel.cancel()]])
    await state.update_data(parameter=parameter, label=label)
    await callback.message.delete()
    await state.update_data(bot_message=await callback.message.answer(text, reply_markup=keyboard))
    await callback.answer()
    await state.set_state(ChangeFields.active)


@_base.message(ChangeFields.active, get_parameters=("key",))
async def _change_active(message: Message, state: FSMContext, **kwargs) -> None:
    parameter: str = await state.get_value("parameter")
    label: str = await state.get_value("label")
    bot_message: Message = await state.get_value("bot_message")
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        await database.parameter(db, kwargs["key"], label, parameter, message.text)
        await db.commit()
    await bot_message.delete()
    await _info.record(message.from_user.id, label)
    await state.clear()
