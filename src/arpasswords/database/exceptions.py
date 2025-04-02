import logging

from ..exceptions import ARPasswordsException

from .. import logger


class DatabaseException(ARPasswordsException):
    pass


class LabelNotUnique(DatabaseException):
    def __init__(self, user_id: int, label: str) -> None:
        self.user_id: int = user_id
        self.label: str = label


    async def log(self) -> None:
        await logger.user(logging.DEBUG, self.user_id, "label_not_unique", label=self.label)
