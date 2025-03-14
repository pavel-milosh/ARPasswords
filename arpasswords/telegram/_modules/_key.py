import asyncio
import datetime

import keyring
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from .. import _base
from ...local import _ as local


class AddKey(StatesGroup):
    active: State = State()
    bot_message: Message


@_base.message(Command("key"), ignore_key=True, get_parameters=("key",))
async def _key(message: Message, state: FSMContext, **kwargs) -> None:
    if kwargs["key"] is None:
        hours: str = await local("c_key", "empty")
    else:
        hours: str = f"около {24 - datetime.datetime.now().hour}"
    button_text: str = (await local("common", "change_?")).format(parameter=await local("parameters", "key"))
    text: str = (await local("c_key", "initial")).format(key=kwargs["key"], hours=hours)
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=button_text, callback_data="change_key")]]
    )
    bot_message: Message = await message.answer(text, reply_markup=keyboard)
    await state.update_data(bot_message=bot_message)
    await asyncio.sleep(120)
    await bot_message.delete()


@_base.router.callback_query(F.data == "change_key")
async def _change_key(callback: CallbackQuery, state: FSMContext) -> None:
    message: Message = await callback.message.answer(await local("c_key", "enter"))
    await state.update_data(bot_message=message)
    await state.set_state(AddKey.active)
    await callback.answer()


@_base.message(AddKey.active, ignore_key=True)
async def _key_set(message: Message, state: FSMContext) -> None:
    data: dict = await state.get_data()
    bot_message: Message = data["bot_message"]
    if len(message.text) < 8:
        try:
            await bot_message.edit_text(await local("c_key", "incorrect"))
        except TelegramBadRequest:
            pass
        finally:
            return

    await asyncio.to_thread(keyring.set_password, "keys", str(message.from_user.id), message.text)
    await state.clear()
    await bot_message.edit_text((await local("c_key", "installed")).format(key=message.text))
    await asyncio.sleep(10)
    await bot_message.delete()
