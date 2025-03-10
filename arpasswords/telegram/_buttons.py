from aiogram.types import InlineKeyboardButton

from ..local import _ as local


async def delete_message(message_id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=local("common", "delete_message"),
        callback_data=f"delete_message {message_id}"
    )