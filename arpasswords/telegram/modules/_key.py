import datetime
import asyncio

import keyring
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from .. import _base, _buttons, _decorators
from ...local import _ as local


class AddKey(StatesGroup):
    active: State = State()
    bot_message: Message


@_base.router.message(Command("key"))
@_decorators.messages_controller(ignore_key=True)
async def _key(message: Message, state: FSMContext) -> None:
    key: str = keyring.get_password("keys", str(message.from_user.id))
    if key is None:
        hours: str = local("c_key", "none")
    else:
        hours: int = 24 - datetime.datetime.now().hour
    bot_message: Message = await message.answer("\u200B")
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=local("common", "change_?").format(
                    parameter=local("common", "key")
                ),
                callback_data="change_key"
            )],
            [await _buttons.delete_message(bot_message.message_id)]
        ]
    )
    await bot_message.edit_text(
        local("c_key", "initial").format(
            key=key,
            hours=hours
        ),
        reply_markup=keyboard
    )
    await state.update_data(bot_message=bot_message)
    await state.set_state(AddKey.active)


@_base.router.message(AddKey.active)
@_decorators.messages_controller(ignore_key=True)
async def _key_set(message: Message, state: FSMContext) -> None:
    key: str = message.text
    data: dict = await state.get_data()
    bot_message: Message = data["bot_message"]
    if len(key) < 8:
        await bot_message.delete()
        await state.update_data(
            bot_message=await message.answer(local("c_key", "incorrect"))
        )
        return
    keyring.set_password("keys", str(message.from_user.id), message.text)
    await bot_message.edit_text(
        local("c_key", "installed").format(
            key=keyring.get_password("keys", str(message.from_user.id))
        ),
    )
    await asyncio.sleep(10)
    await bot_message.edit_text(local("c_key", "done"))
    await state.clear()