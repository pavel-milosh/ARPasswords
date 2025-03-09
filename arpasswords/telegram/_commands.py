import html

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from . import _base, _decorators
from .. import core, localization


@_base.dp.message(Command("start"))
@_decorators.message_checker(ignore_key=True)
async def _start(message: Message) -> None:
    await message.answer(localization.start(message.from_user.first_name))


@_base.dp.message(Command("generate_password"))
async def _generate_password(message: Message) -> None:
    password: str = html.escape(core.password.generate())
    bot_message: Message = await message.answer(
        localization.generate_password.generating
    )
    button: InlineKeyboardButton= InlineKeyboardButton(
        text=localization.generate_password.delete,
        callback_data=f"delete_message {bot_message.message_id}"
    )
    await bot_message.edit_text(
        localization.generate_password.initial(password),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[button]])
    )
