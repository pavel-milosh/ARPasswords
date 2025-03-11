import asyncio
import functools
import os
from typing import Callable

import keyring
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Message

from .. import database
from ..config import _ as config
from ..local import _ as local


bot: Bot = Bot(config()["token"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
_dp: Dispatcher = Dispatcher()
router: Router = Router()


def message(*args, ignore_key: bool = False, get_parameters: tuple[str, ...] = (), **kwargs) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @router.message(*args, **kwargs)
        async def wrapper(message: Message, *args, **kwargs) -> Callable:
            key: str = await asyncio.to_thread(keyring.get_password,"keys", str(message.from_user.id))

            if "key" in get_parameters:
                kwargs["key"] = key

            if not os.path.exists(os.path.join("users", f"{message.from_user.id}.db")):
                await database.create(message.from_user.id)

            if not ignore_key and key is None:
                await message.reply(await local("c_key", "install"))
            else:
                await message.delete()
                return await func(message, *args, **kwargs)
        return wrapper
    return decorator


async def start() -> None:
    # noinspection PyProtectedMember
    commands: dict[str, str] = dict((await local("commands"))._catalog)
    await bot.set_my_commands(
        [
            BotCommand(command=key, description=value)
            for key, value in commands.items()
            if key
        ]
    )
    _dp.include_router(router)
    await _dp.start_polling(bot)
