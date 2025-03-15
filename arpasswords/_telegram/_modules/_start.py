from aiogram.filters import Command
from aiogram.types import Message

from .. import _base
from ..._local import _ as _local


@_base.message(Command("start"), ignore_key=True)
async def _start(message: Message) -> None:
    text: str = (await _local("commands", "start_message")).format(name=message.from_user.first_name)
    await message.answer(text)
