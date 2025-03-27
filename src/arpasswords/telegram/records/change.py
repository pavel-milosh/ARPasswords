import os
import re
from collections import Counter

import aiosqlite
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from . import info
from .. import base, cancel, password
from ... import database
from ...config import _ as config
from ...lang import _ as lang


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


@base.router.callback_query(F.data.startswith("change_parameter"))
async def _change_parameter(callback: CallbackQuery) -> None:
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    buttons: list[list[InlineKeyboardButton]] = []
    for parameter in config()["parameters"]:
        value: str = await lang("parameters", parameter)
        button_text: str = (await lang("change", "parameter?")).format(parameter=value)
        callback_data: str = f"change_{parameter} {label}"
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])
    await callback.message.answer(
        await lang("change", "which_parameter"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await callback.answer(await lang("common", "request_operated"))


@base.alt_router.callback_query(F.data.startswith("change_"))
async def _change(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    buttons: list[list[InlineKeyboardButton]] = []
    label: str = callback.data[callback.data.find(" ") + 1:]
    parameter: str = callback.data.split()[0].replace("change_", "")
    parameter_text: str = (await lang("parameters", parameter)).capitalize()
    text: str = (await lang("change", "new_value_for_parameter")).format(parameter=parameter_text)
    if parameter == "password":
        text += "\n" + (await lang("change", "suggest_password")).format(password=await password.generate())
    elif parameter == "backup_codes":
        text += "\n" + await lang("change", "backup_codes")
    elif parameter in ("email", "phone"):
        async with aiosqlite.connect(os.path.join("users", f"{callback.from_user.id}.db")) as db:
            values: list[str] = await database.values(db, parameter, callback.from_user.id)
        most_common_values: list[str] = list(dict(Counter(values).most_common()).keys())
        for value in most_common_values:
            buttons.append([InlineKeyboardButton(text=value, callback_data=f"quick {value}")])
    buttons.append([InlineKeyboardButton(text=await lang("change", "empty"), callback_data="quick None")])
    buttons.append([await cancel.button()])
    bot_message: Message = await callback.message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.update_data(parameter=parameter, label=label)
    await state.update_data(bot_message=bot_message)
    await state.set_state(ChangeFields.active)
    await callback.answer(await lang("common", "request_operated"))


@base.message(ChangeFields.active)
@base.router.callback_query(F.data.startswith("quick"))
async def _change_active(object: Message | CallbackQuery, state: FSMContext) -> None:
    if isinstance(object, CallbackQuery):
        value: str | list[str] = object.data[object.data.find(" ") + 1:]
    else:
        value: str | list[str] = object.text
    parameter: str = await state.get_value("parameter")
    label: str = await state.get_value("label")
    bot_message: Message = await state.get_value("bot_message")
    if value.lower() != "none":
        if parameter == "phone":
            value = format_phone(value)
        elif parameter == "totp":
            value = value.replace(" ", "")
        elif parameter == "backup_codes":
            value = value.split("\n")
    async with aiosqlite.connect(os.path.join("users", f"{object.from_user.id}.db")) as db:
        await database.parameter(db, object.from_user.id, label, parameter, value)
        await db.commit()
    await state.clear()
    await bot_message.delete()
    if parameter == "label":
        await info.record(object.from_user.id, value)
    else:
        await info.record(object.from_user.id, label)
