import os

from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from .. import base
from ...lang import _ as lang


@base.message(Command("backup"))
async def _backup(message: Message) -> None:
    filename: str = os.path.join("users", f"{message.from_user.id}.db")
    size: int = int(os.path.getsize(filename) / 1024**2)
    if size > 50:
        await message.answer(await lang("command", "backup_very_large"))
        return
    file: FSInputFile = FSInputFile(filename)
    bot_message: Message = await message.answer(await lang("commands", "backup_uploading"))
    await base.bot.send_document(message.from_user.id, file, caption=await lang("commands", "backup_done"))
    await bot_message.delete()
