import asyncio
import logging
import os

import aiosqlite
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from . import base, cancel
from .. import database, logger
from ..exceptions import Decryption
from ..config import _ as config
from ..keys import _ as keys
from ..lang import _ as lang


class EnterKey(StatesGroup):
    active: State = State()
    bot_message: Message


@base.message(Command("key"), ignore_key=True)
async def _key(message: Message, state: FSMContext) -> None:
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=await lang("commands", "key_button"), callback_data="enter_key")]
    ]
    text: str = (await lang("commands", "key_message")).format(key=await keys.get(message.from_user.id), time=keys.time)
    bot_message = await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.update_data(bot_message=bot_message)
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass


@base.router.callback_query(F.data == "enter_key")
async def _enter_key(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    message: Message = await callback.message.answer(
        await lang("commands", "key_enter"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[await cancel.button()]])
    )
    await state.update_data(bot_message=message)
    await state.set_state(EnterKey.active)
    await callback.answer(await lang("common", "request_operated"))


@base.message(EnterKey.active, ignore_key=True)
async def _enter_key_active(message: Message, state: FSMContext) -> None:
    data: dict = await state.get_data()
    bot_message: Message = data["bot_message"]
    if len(message.text) < 8:
        try:
            await bot_message.edit_text(
                await lang("common", "incorrect_value"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[await cancel.button()]])
            )
        except TelegramBadRequest:
            pass
        finally:
            return
    await keys.set(message.from_user.id, message.text)
    async with aiosqlite.connect(os.path.join("users", f"{message.from_user.id}.db")) as db:
        checked: bool = False
        try:
            for label in await database.values(db, "label"):
                for parameter in config()["parameters"]+ await database.additional_parameters(db, message.from_user.id, label):
                    value: str | list[str] | None = await database.parameter(db, message.from_user.id, label, parameter)
                    if parameter != "label" and value is not None:
                        checked = True
                        break
                if checked:
                    break
        except Decryption:
            try:
                await bot_message.edit_text(
                    await lang("commands", "key_wrong"),
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[await cancel.button()]])
                )
                await logger.user(logging.INFO, message.from_user.id, "key_wrong")
            except TelegramBadRequest:
                pass
            finally:
                keys.delete(message.from_user.id)
                return
    await state.clear()
    await bot_message.edit_text((await lang("commands", "key_installed")).format(key=message.text))
    await logger.user(logging.INFO, message.from_user.id, "key_installed")
    await asyncio.sleep(10)
    await bot_message.delete()
