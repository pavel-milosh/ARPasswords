from aiogram.types import Message
from aiogram.filters import Command

from .. import _base
from ...local import _ as local


@_base.message(Command("start"), ignore_key=True)
async def _command(message: Message) -> None:
    await message.answer(local("c_start", "initial").format(name=message.from_user.first_name))
