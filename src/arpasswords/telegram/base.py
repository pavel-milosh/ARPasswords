import asyncio
import functools
import os
from typing import Any, Callable

import aiofiles.os
import keyring
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Message

from .. import database
from ..config import _ as config
from ..lang import _ as lang


bot: Bot = Bot(config()["token"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router: Router = Router()
alt_router: Router = Router()
_dp: Dispatcher = Dispatcher()


def message(*args, router: Router = router, ignore_key: bool = False, **kwargs) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @router.message(*args, **kwargs)
        async def wrapper(message: Message, **kwargs) -> Any:
            key: str | None = await asyncio.to_thread(keyring.get_password, "keys", str(message.from_user.id))
            if not await aiofiles.os.path.exists(os.path.join("users", f"{message.from_user.id}.db")):
                await database.create(message.from_user.id)
            if not ignore_key and key is None:
                await message.reply(await lang("commands", "key_not_installed"))
                return
            await message.delete()
            # noinspection PyUnresolvedReferences
            filtered_kwargs = {key: valuer for key, valuer in kwargs.items() if key in func.__annotations__}
            return await func(message, **filtered_kwargs)
        return wrapper
    return decorator


async def start() -> None:
    commands: list[str] = config()["commands"]
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=await lang("commands", command))
            for command in commands
        ]
    )
    _dp.include_routers(router, alt_router)
    await _dp.start_polling(bot)
