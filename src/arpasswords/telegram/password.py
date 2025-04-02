import asyncio
import logging
import html

from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message

from . import base
from .. import logger, utilities
from ..lang import _ as lang


@base.message(Command("generate_passwords"), ignore_key=True)
async def _generate_passwords(message: Message) -> None:
    passwords: list[str] = [f"\t\t• <code>{html.escape(await utilities.password.generate())}</code>" for _ in range(10)]
    text: str = (await lang("commands", "generate_passwords_message")).format(passwords="\n".join(passwords))
    bot_message: Message = await message.answer(text)
    await logger.user(logging.INFO, message.from_user.id, "passwords_generated")
    await asyncio.sleep(60**2)
    try:
        await bot_message.delete()
    except TelegramBadRequest:
        pass
