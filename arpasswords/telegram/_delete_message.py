from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton

from . import _base
from ..local import _ as local


async def button(message_id: int) -> InlineKeyboardButton:
    text: str = await local("common", "delete_message")
    callback_data: str = f"delete_message {message_id}"
    return InlineKeyboardButton(text=text, callback_data=callback_data)


@_base.router.callback_query(F.data.startswith("delete_message"))
async def _callback(callback: CallbackQuery) -> None:
    message_id: int = int(callback.data.split()[1])
    await _base.bot.delete_message(callback.message.chat.id, message_id)
