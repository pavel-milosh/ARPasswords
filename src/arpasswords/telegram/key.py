import asyncio
import datetime

import keyring
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from . import base, cancel
from ..lang import _ as lang


class EnterKey(StatesGroup):
    active: State = State()
    bot_message: Message


@base.message(Command("key"), ignore_key=True)
async def _key(message: Message, state: FSMContext) -> None:
    key: str | None = await asyncio.to_thread(keyring.get_password, "keys", str(message.from_user.id))
    buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=await lang("commands", "key_button"), callback_data="enter_key")]
    ]
    text: str = (await lang("commands", "key_message")).format(key=key, hours=24 - datetime.datetime.now().hour)
    bot_message = await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.update_data(bot_message=bot_message)
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass


@base.router.callback_query(F.data == "enter_key")
async def _enter_key(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    message: Message = await callback.message.answer(
        await lang("commands", "key_enter"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[await cancel.button()]])
    )
    await state.update_data(bot_message=message)
    await state.set_state(EnterKey.active)


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
    await state.clear()
    await asyncio.to_thread(keyring.set_password, "keys", str(message.from_user.id), message.text)
    await bot_message.edit_text((await lang("commands", "key_installed")).format(key=message.text))
    await asyncio.sleep(10)
    await bot_message.delete()
