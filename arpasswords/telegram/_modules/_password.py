import asyncio
import html
import string
import secrets

from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import Command

from .. import _base, _delete_message
from ...local import _ as local


def _s_generate(length: int = 20) -> str:
    power: int = 0
    password: str = ""
    while power < 3:
        password = "".join(
            [
                secrets.choice(string.ascii_letters + string.digits + string.punctuation)
                for _ in range(length)
            ]
        )
        power = (any(letter in password for letter in string.ascii_letters) +
                      any(digit in password for digit in string.digits)+
                      any(char in password for char in string.punctuation))

    return password


async def _generate(length: int = 20) -> str:
    return await asyncio.to_thread(_s_generate, length=length)


@_base.message(Command("generate_password"), ignore_key=True)
async def _command(message: Message) -> None:
    password: str = html.escape(await _generate())
    bot_message: Message = await message.answer(".")
    await bot_message.edit_text(
        local("c_generate_password", "initial").format(password=password),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[await _delete_message.button(bot_message.message_id)]]
        )
    )