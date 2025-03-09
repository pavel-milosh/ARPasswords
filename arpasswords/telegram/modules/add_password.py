from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .. import _base, _decorators
from ... import localization


class AddPassword(StatesGroup):
    label_state: State = State()
    password_state: State = State()
    label: str
    password: str
    url: str = None
    totp: str = None
    backup_codes: list[str] | None = None
    bot_message: Message
    user_message: Message


@_base.dp.message(Command("add_password"))
@_decorators.message_checker()
async def _add_password(message: Message, state: FSMContext) -> None:
    await state.set_state(AddPassword.label_state)
    await state.update_data(
        bot_message=await message.answer(localization.add_password.initial)
    )


@_base.dp.message(AddPassword.label_state)
@_decorators.message_checker()
async def _add_password_label(message: Message, state: FSMContext) -> None:
    await state.set_state(AddPassword.password_state)
    await state.update_data(label=message.text)
    bot_message: Message = await state.get_value("bot_message")
    await bot_message.edit_text(localization.add_password.enter_password)
    await message.delete()


@_base.dp.message(AddPassword.password_state)
@_decorators.message_checker()
async def _add_password_password(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    text: str = localization.add_password.info(
        await state.get_value("label"),
        await state.get_value("password"),
        await state.get_value("url"),
        await state.get_value("totp"),
        await state.get_value("backup_codes")
    )
    await message.answer(text)
    await message.delete()
