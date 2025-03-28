import os

import aiosqlite
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from . import info
from .. import base, cancel
from ... import database
from ...config import _ as config
from ...database.exceptions import LabelNotUnique
from ...lang import _ as lang


class AddRecord(StatesGroup):
    active: State = State()
    bot_message: Message


@base.message(Command("add"))
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
            await bot_message.edit_text(await lang("records", "label_not_unique"), reply_markup=keyboard)
            return
        await db.commit()
    await state.clear()
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
    finally:
        await info.record(message.from_user.id, message.text)


@base.router.callback_query(F.data.startswith("add_parameter"))
async def _add_parameter(callback: CallbackQuery) -> None:
    await callback.message.delete()
    label: str = callback.data[callback.data.find(" ") + 1:]
    buttons: list[list[InlineKeyboardButton]] = []
    async with aiosqlite.connect(os.path.join("users", f"{callback.from_user.id}.db")) as db:
        additional_parameters: list[str] = await database.additional_parameters(db, callback.from_user.id, label)
    for parameter in config()["additional_parameters"]:
        if parameter not in additional_parameters:
            text: str = (await lang("parameters", parameter)).capitalize()
            buttons.append([InlineKeyboardButton(text=text, callback_data=f"edit_{parameter} {label}")])
    await callback.message.answer(await lang("records", "choose_parameter"), reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer(await lang("common", "request_operated"))
