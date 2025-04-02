import asyncio
import logging
import os
from logging import FileHandler, Formatter, Logger

from .lang import _ as lang


_main_logger: Logger = logging.getLogger("arpasswords")
_main_file_handler: FileHandler = FileHandler("arpasswords.log")
_formatter: Formatter = Formatter("[%(asctime)s] [%(levelname)s]: %(message)s")

_user_loggers: dict[int, Logger] = {}


def _add_logger(user_id: int) -> None:
    file_handler: FileHandler = FileHandler(os.path.join("users", f"{user_id}.log"))
    file_handler.setFormatter(_formatter)
    _user_loggers[user_id] = logging.getLogger(str(user_id))
    _user_loggers[user_id].setLevel(logging.DEBUG)
    _user_loggers[user_id].addHandler(file_handler)


async def add_logger(user_id: int) -> None:
    await asyncio.to_thread(_add_logger, user_id)
    await user(logging.INFO, user_id, "first_launch")
    await main(logging.INFO, "new_user")


async def main(level: int, code: str, exc_info: bool = False, **kwargs) -> None:
    if kwargs:
        text: str = (await lang("main_logger", code)).format(**kwargs)
    else:
        text: str = await lang("main_logger", code)
    # noinspection PyTypeChecker
    await asyncio.to_thread(_main_logger.log, level, text, exc_info=exc_info)


async def user(level: int, user_id: int, code: str, exc_info: bool = False, **kwargs) -> None:
    if user_id not in _user_loggers:
        await add_logger(user_id)
    if kwargs:
        text: str = (await lang("logger", code)).format(**kwargs)
    else:
        text: str = await lang("logger", code)
    # noinspection PyTypeChecker
    await asyncio.to_thread(_user_loggers[user_id].log, level, text, exc_info=exc_info)


async def setup() -> None:
    _main_file_handler.setFormatter(_formatter)
    _main_logger.setLevel(logging.INFO)
    _main_logger.addHandler(_main_file_handler)
    await main(logging.INFO, await lang("logger", "started"))
