import asyncio
import os

import aiosqlite
import keyring
from aiogram import F
from aiogram.types import CallbackQuery, Message
from pyotp import TOTP

from ... import _base
from .... import database
from ....local import _ as local


def _c_get_otp(totp: str) -> str:
    totp: TOTP = TOTP(totp)
    return totp.now()


async def _get_otp(totp: str) -> str:
    return await asyncio.to_thread(_c_get_otp, totp)


@_base.router.callback_query(F.data.startswith("otp"))
async def _totp(callback: CallbackQuery) -> None:
    await callback.answer()
    key: str = await asyncio.to_thread(keyring.get_password,"keys", str(callback.from_user.id))
    label: str = callback.data[callback.data.find(" ") + 1:]
    async with aiosqlite.connect(os.path.join("users", f"{callback.from_user.id}.db")) as db:
        totp: str = await database.parameter(db, key, label, "totp")
    otp: str = await _get_otp(totp)
    text: str = (await local("otp", "initial")).format(OTP=otp)
    message: Message = await callback.message.answer(text)
    await asyncio.sleep(30)
    await message.delete()
