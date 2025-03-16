import asyncio
from asyncio import AbstractEventLoop

from . import telegram
from .local import _ as local


class ARPasswordsException(Exception):
    pass


class EncryptionException(ARPasswordsException):
    pass


class DecryptionException(ARPasswordsException):
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id


    async def message(self) -> None:
        await telegram.base.bot.send_message(self.user_id, await local("exceptions", "decrypt"))
