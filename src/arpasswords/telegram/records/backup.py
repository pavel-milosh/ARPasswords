import logging
import os

from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from .. import base
from ... import logger
from ...lang import _ as lang


@base.message(Command("backup"))
async def _backup(message: Message) -> None:
    db_filename: str = os.path.join("users", f"{message.from_user.id}.db")
    log_filename: str = os.path.join("users", f"{message.from_user.id}.log")
    size: int = int(os.path.getsize(db_filename) / 1024**2)
    if size > 50:
        await message.answer(await lang("command", "backup_very_large"))
        return
    db: FSInputFile = FSInputFile(db_filename)
    log: FSInputFile = FSInputFile(log_filename)
    bot_message: Message = await message.answer(await lang("commands", "backup_uploading"))
    await base.bot.send_document(message.from_user.id, db, caption=await lang("commands", "backup_db"))
    await base.bot.send_document(message.from_user.id, log, caption=await lang("commands", "backup_log"))
    await logger.user(logging.INFO, message.from_user.id, "backup_done")
    await bot_message.delete()
