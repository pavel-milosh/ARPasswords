import os

import keyring
import aiosqlite
from aiogram import F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from ... import _base, _buttons
from .... import database
from ....local import _ as local


@_base.router.callback_query(F.data.startswith("record_info"))
async def _callback_record_info(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await record(callback.from_user.id, callback.data.split()[1])


async def record(user_id: int, label: str) -> None:
    key: str = keyring.get_password("keys", str(user_id))
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        login: str = await database.records.login(db, key, label)
        email: str = await database.records.email(db, key, label)
        phone: str = await database.records.phone(db, key, label)
        password: str = await database.records.password(db, key, label)
        url: str = await database.records.url(db, key, label)
        totp: str = await database.records.totp(db, key, label)
        backup_codes: list[str] = await database.records.backup_codes(db, key, label)

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
    bot_message: Message = await _base.bot.send_message(user_id, "\u200B")
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
    buttons.insert(0, [await _buttons.delete_message(bot_message.message_id)])
    await bot_message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
