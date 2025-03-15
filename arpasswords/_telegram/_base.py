import asyncio
import functools
import os
from typing import Any, Callable

import keyring
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Message

from .. import _database
from .._config import _ as _config
from .._local import _ as _local


bot: Bot = Bot(_config()["token"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
_dp: Dispatcher = Dispatcher()
router: Router = Router()
alt_router: Router = Router()


def message(*args, router: Router = router, ignore_key: bool = False, get_parameters: tuple[str, ...] = (), **kwargs) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @router.message(*args, **kwargs)
        async def wrapper(message: Message, **kwargs) -> Any:
            key: str | None = await asyncio.to_thread(keyring.get_password, "keys", str(message.from_user.id))

            c_kwargs: dict[str, Any] = {}
            if "key" in get_parameters:
                c_kwargs["key"] = key

            if not os.path.exists(os.path.join("users", f"{message.from_user.id}.db")):
                await _database.create(message.from_user.id)

            if not ignore_key and key is None:
                await message.reply(await _local("key", "need_install"))
                return

            await message.delete()

            # noinspection PyUnresolvedReferences
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in func.__annotations__}
            return await func(message, **filtered_kwargs | c_kwargs)
        return wrapper
    return decorator

async def start() -> None:
    commands: list[str] = _config()["commands"]
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=await _local("commands", command))
            for command in commands
        ]
    )
    _dp.include_routers(router, alt_router)
    await _dp.start_polling(bot)
