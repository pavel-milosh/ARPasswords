from . import telegram
from .lang import _ as lang


class ARPasswordsException(Exception):
    pass


class EncryptionException(ARPasswordsException):
    pass


class DecryptionException(ARPasswordsException):
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id


    async def message(self) -> None:
        await telegram.base.bot.send_message(self.user_id, await lang("exceptions", "decrypt"))
