import functools
import os
from typing import Callable

import keyring
from aiogram.types import Message

from .. import database


def messages_controller(*, ignore_key: bool = False) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(message: Message, *args: tuple, **kwargs: dict) -> Callable:
            user_id: int = message.from_user.id
            if not os.path.exists(os.path.join("users", f"{user_id}.db")):
                await database.create(user_id)

            if not ignore_key and keyring.get_password("keys", str(user_id)) is None:
                await message.reply(
                    "Необходимо установить ключ шифрования! "
                    "Воспользуйтесь командой /key"
                )
            else:
                await message.delete()
                return await func(message, *args, **kwargs)
        return wrapper
    return decorator