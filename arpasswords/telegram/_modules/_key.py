import asyncio
import datetime

import keyring
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from . import _cancel
from .. import _base
from ...local import _ as local


class AddKey(StatesGroup):
    active: State = State()
    bot_message: Message


@_base.message(Command("key"), ignore_key=True, get_parameters=("key",))
async def _key(message: Message, state: FSMContext, **kwargs) -> None:
    if kwargs["key"] is None:
        hours: str = await local("key", "empty")
    else:
        hours: str = f"около {24 - datetime.datetime.now().hour}"
    button_text: str = (await local("change", "parameter?")).format(parameter=await local("parameters", "key"))
    text: str = (await local("key", "initial")).format(key=kwargs["key"], hours=hours)
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=button_text, callback_data="change_key")]]
    )
    bot_message: Message = await message.answer(text, reply_markup=keyboard)
    await state.update_data(bot_message=bot_message)
    await asyncio.sleep(120)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass


@_base.router.callback_query(F.data == "change_key")
async def _change_key(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    parameter: str = (await local("parameters", "key")).capitalize()
    text: str = (await local("change", "new_value_for_parameter")).format(parameter=parameter)
    message: Message = await callback.message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[await _cancel.button()]]))
    await state.update_data(bot_message=message)
    await state.set_state(AddKey.active)


@_base.message(AddKey.active, ignore_key=True)
async def _key_set(message: Message, state: FSMContext) -> None:
    data: dict = await state.get_data()
    bot_message: Message = data["bot_message"]
    if len(message.text) < 8:
        try:
            await bot_message.edit_text(await local("common", "incorrect_value"))
        except TelegramBadRequest:
            pass
        finally:
            return
    await state.clear()
    await asyncio.to_thread(keyring.set_password, "keys", str(message.from_user.id), message.text)
    await bot_message.edit_text((await local("key", "installed")).format(key=message.text))
    await asyncio.sleep(10)
    await bot_message.delete()
