import functools
import os
from typing import Callable

import keyring
import aiosqlite
from aiogram.types import Message


def message_checker(*, ignore_key: bool = False) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(message: Message, *args: tuple, **kwargs: dict) -> Callable:
            user_id: int = message.from_user.id
            if not os.path.exists(os.path.join("users", f"{user_id}.db")):
                async with aiosqlite.connect(
                        os.path.join("users", f"{user_id}.db")
                ) as db:
                    await db.execute(
                        "CREATE TABLE passwords "
                        "("
                            "label TEXT NOT NULL PRIMARY KEY,"
                            "encrypted_password TEXT NOT NULL,"
                            "url TEXT,"
                            "encrypted_totp TEXT,"
                            "encrypted_backup_codes TEXT"
                        ")"
                    )
                    await db.commit()

            if not ignore_key and keyring.get_password("keys", str(user_id)) is None:
                await message.reply(
                    "Необходимо установить ключ шифрования! "
                    "Воспользуйтесь командой /key"
                )
            else:
                return await func(message, *args, **kwargs)
        return wrapper
    return decorator