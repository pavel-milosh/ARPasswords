from aiogram import F
from aiogram.types import CallbackQuery

from . import _base


@_base.router.callback_query(F.data.startswith("delete_message"))
async def _delete_message(callback: CallbackQuery) -> None:
    message_id: int = int(callback.data.split()[1])
    await _base.bot.delete_message(callback.message.chat.id, message_id)
