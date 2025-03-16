from aiogram.filters import Command
from aiogram.types import Message

from .. import base
from ...locale import _ as locale


@base.message(Command("start"), ignore_key=True)
async def _start(message: Message) -> None:
    text: str = (await locale("commands", "start_message")).format(name=message.from_user.first_name)
    await message.answer(text)
