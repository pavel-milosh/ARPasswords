import asyncio
import html
import secrets
import string

from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from .. import _base, _delete_message
from ...local import _ as local


def _s_generate(length: int = 20) -> str:
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


async def _generate(length: int = 20) -> str:
    return await asyncio.to_thread(_s_generate, length=length)


@_base.message(Command("generate_password"), ignore_key=True)
async def _command(message: Message) -> None:
    password: str = html.escape(await _generate())
    bot_message: Message = await message.answer(".")
    text: str = (await local("c_generate_password", "initial")).format(password=password)
    button: InlineKeyboardButton = await _delete_message.button(bot_message.message_id)
    await bot_message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[button]]))
