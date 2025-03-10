import html

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from . import _base, _decorators
from .. import generate
from ..local import _ as local


@_base.dp.message(Command("start"))
@_decorators.messages_controller(ignore_key=True)
async def _start(message: Message) -> None:
    await message.answer(local("c_start", "initial").format(name=message.from_user.first_name))


@_base.dp.message(Command("generate_password"))
@_decorators.messages_controller(ignore_key=True)
async def _generate_password(message: Message) -> None:
    password: str = html.escape(generate.password())
    bot_message: Message = await message.answer(
        local("c_generate_password", "generating")
    )
    button: InlineKeyboardButton= InlineKeyboardButton(
        text=local("common", "delete_message"),
        callback_data=f"delete_message {bot_message.message_id}"
    )
    await bot_message.edit_text(
        local("c_generate_password", "initial").format(password=password),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[button]])
    )
