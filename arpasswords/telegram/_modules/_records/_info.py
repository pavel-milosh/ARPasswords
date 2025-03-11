import asyncio
import os

import keyring
import aiosqlite
from aiogram import F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from ... import _base, _delete_message
from .... import database
from ....local import _ as local


@_base.router.callback_query(F.data.startswith("record_info"))
async def _callback_record_info(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await record(callback.from_user.id, callback.data.split()[1])


async def record(user_id: int, label: str) -> None:
    key: str = await asyncio.to_thread(keyring.get_password,"keys", str(user_id))
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        login: str | None = await database.parameter(db, key, label, "login")
        email: str | None = await database.parameter(db, key, label, "email")
        phone: str | None = await database.parameter(db, key, label, "phone")
        password: str | None = await database.parameter(db, key, label, "password")
        url: str | None = await database.parameter(db, key, label, "url")
        totp: str | None = await database.parameter(db, key, label, "totp")
        backup_codes: list[str] | None = await database.parameter(db, key, label, "backup_codes")

    text: str = local("records", "info").format(
        label=label,
        login=login,
        email=email,
        phone=phone,
        password=password,
        url=url,
        totp=totp,
        backup_codes=backup_codes
    )
    bot_message: Message = await _base.bot.send_message(user_id, ".")
    # noinspection PyProtectedMember
    buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=local("common", "change_?").format(parameter=value),
                callback_data=f"change_{key} {label}"
            )
        ]
        for key, value in dict(local("parameters")._catalog).items()
        if key not in ("", "label", "key")
    ]
    buttons.insert(0, [await _delete_message.button(bot_message.message_id)])
    await bot_message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
