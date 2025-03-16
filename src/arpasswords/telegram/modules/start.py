from aiogram.filters import Command
from aiogram.types import Message

from .. import base
from ...lang import _ as lang


@base.message(Command("start"), ignore_key=True)
async def _start(message: Message) -> None:
    text: str = (await lang("commands", "start_message")).format(name=message.from_user.first_name)
    await message.answer(text)
