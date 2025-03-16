from . import telegram
from .locale import _ as locale


class ARPasswordsException(Exception):
    pass


class EncryptionException(ARPasswordsException):
    pass


class DecryptionException(ARPasswordsException):
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id


    async def message(self) -> None:
        await telegram.base.bot.send_message(self.user_id, await locale("exceptions", "decrypt"))
