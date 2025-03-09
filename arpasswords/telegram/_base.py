from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .. import config, localization


bot: Bot = Bot(
    config.telegram().token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp: Dispatcher = Dispatcher()


async def start_polling() -> None:
    await bot.set_my_commands(localization.commands)
    await dp.start_polling(bot)
