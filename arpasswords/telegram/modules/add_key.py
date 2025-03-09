import asyncio

import keyring
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command

from .. import _base, _decorators
from ... import localization


class AddKey(StatesGroup):
    active: State = State()
    bot_message: Message


@_base.dp.message(Command("key"))
@_decorators.message_checker(ignore_key=True)
async def _key(message: Message, state: FSMContext) -> None:
    await state.update_data(
        bot_message=await message.answer(localization.key.initial)
    )
    await state.set_state(AddKey.active)


@_base.dp.message(AddKey.active)
@_decorators.message_checker(ignore_key=True)
async def _key_set(message: Message, state: FSMContext) -> None:
    key: str = message.text
    data: dict = await state.get_data()
    bot_message: Message = data["bot_message"]
    if len(key) < 8:
        await bot_message.delete()
        await state.update_data(
            bot_message=await message.answer(localization.key.incorrect)
        )
        await message.delete()
        return
    keyring.set_password("keys", str(message.from_user.id), message.text)
    await bot_message.edit_text(
        localization.key.deleting(
            keyring.get_password("keys", str(message.from_user.id))
        )
    )
    await asyncio.sleep(10)
    await message.delete()
    await bot_message.edit_text(localization.key.done)