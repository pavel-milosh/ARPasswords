import asyncio
import html
import secrets
import string

from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message

from .. import base
from ...lang import _ as lang


def _generate(length: int = 20) -> str:
    while True:
        password: str = ""
        for _ in range(length):
            password += secrets.choice(string.ascii_letters + string.digits + string.punctuation)

        has_upper_letters: bool = any(char in password for char in string.ascii_uppercase)
        has_lower_letters: bool = any(char in password for char in string.ascii_lowercase)
        has_digits: bool = any(char in password for char in string.digits)
        has_punctuation: bool = any(char in password for char in string.punctuation)
        power: int = has_upper_letters + has_lower_letters + has_digits + has_punctuation

        if power == 4:
            return password


async def generate(length: int = 20) -> str:
    return await asyncio.to_thread(_generate, length=length)


@base.message(Command("generate_passwords"), ignore_key=True)
async def _command(message: Message) -> None:
    passwords: list[str] = [f"\t\t• <code>{html.escape(await generate())}</code>" for _ in range(10)]
    text: str = (await lang("commands", "generate_password_message")).format(passwords="\n".join(passwords))
    await message.answer(text)
    await asyncio.sleep(60**2)
    try:
        await message.delete()
    except TelegramBadRequest:
        pass
