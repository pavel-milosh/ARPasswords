from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from .. import config
from ..local import _ as local


bot: Bot = Bot(
    config.telegram().token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp: Dispatcher = Dispatcher()
router: Router = Router()


async def start_polling() -> None:
    # noinspection PyProtectedMember
    commands: dict[str, str] = dict(local("commands")._catalog)
    await bot.set_my_commands(
        [
            BotCommand(command=key, description=value)
            for key, value in commands.items()
            if key
        ]
    )
    dp.include_router(router)
    await dp.start_polling(bot)
