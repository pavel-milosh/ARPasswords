import html

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from . import _base, _buttons, _decorators
from .. import generate
from ..local import _ as local


@_base.router.message(Command("start"))
@_decorators.messages_controller(ignore_key=True)
async def _start(message: Message, **kwargs) -> None:
    await message.answer(local("c_start", "initial").format(name=message.from_user.first_name))


@_base.router.message(Command("generate_password"))
@_decorators.messages_controller(ignore_key=True)
async def _generate_password(message: Message, **kwargs) -> None:
    password: str = html.escape(generate.password())
    bot_message: Message = await message.answer(".")
    await bot_message.edit_text(
        local("c_generate_password", "initial").format(password=password),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[await _buttons.delete_message(bot_message.message_id)]]
        )
    )
