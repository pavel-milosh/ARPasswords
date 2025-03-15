import os
import re

import aiosqlite
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from . import _info
from .. import _cancel
from ... import _base
from .... import _database
from ...._config import _ as _config
from ...._local import _ as _local


class ChangeFields(StatesGroup):
    active: State = State()
    bot_message: Message
    label: str
    parameter: str


def format_phone(phone: str) -> str:
    digits: str = re.sub(r"\D", "", phone)
    if len(digits) == 11:
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    elif len(digits) == 10:
        return f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}"


@_base.router.callback_query(F.data.startswith("change_parameter"))
async def _change_parameter(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    buttons: list[list[InlineKeyboardButton]] = []
    for key in _config()["parameters"]:
        if key != "key":
            value: str = await _local("parameters", key)
            button_text: str = (await _local("change", "parameter?")).format(parameter=value)
            callback_data: str = f"change_{key} {label}"
            buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])
    await callback.message.answer(
        await _local("change", "which_parameter"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@_base.alt_router.callback_query(F.data.startswith("change_"))
async def _change(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    parameter: str = callback.data.split()[0].replace("change_", "")
    parameter_text: str = (await _local("parameters", parameter)).capitalize()
    text: str = (await _local("change", "new_value_for_parameter")).format(parameter=parameter_text)
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[await _cancel.button()]])
    await state.update_data(parameter=parameter, label=label)
    await state.update_data(bot_message=await callback.message.answer(text, reply_markup=keyboard))
    await state.set_state(ChangeFields.active)


@_base.message(ChangeFields.active, get_parameters=("key",))
async def _change_active(message: Message, state: FSMContext, **kwargs) -> None:
    parameter: str = await state.get_value("parameter")
    label: str = await state.get_value("label")
    bot_message: Message = await state.get_value("bot_message")
    value: str = message.text
    if parameter == "phone":
        value = format_phone(value)
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        await _database.parameter(db, kwargs["key"], label, parameter, value)
        await db.commit()
    await state.clear()
    await bot_message.delete()
    if parameter == "label":
        await _info.record(message.from_user.id, value)
    else:
        await _info.record(message.from_user.id, label)
