import json

from aiosqlite import Connection

from .. import _base
from ... import crypto


async def _do(
        db: Connection,
        key: str,
        label: str,
        parameter: str,
        value: str | None = None
) -> str | None:
    if value is None:
        encrypted: str | None = await _base.get(db, "passwords", label, parameter)
        if encrypted:
            return crypto.decrypt(encrypted, key)
    else:
        await _base.set(db, "passwords", label, parameter, crypto.encrypt(value, key))


async def parameter(
        db: Connection,
        parameter: str,
        key: str,
        label: str,
        value: str | None = None
) -> str | None:
    if parameter == "login":
        return await login(db, key, label, value)
    if parameter == "email":
        return await email(db, key, label, value)
    if parameter == "password":
        return await password(db, key, label, value)
    if parameter == "phone":
        return await phone(db, key, label, value)
    if parameter == "url":
        return await url(db, key, label, value)
    if parameter == "totp":
        return await totp(db, key, label, value)


async def labels(db: Connection) -> list[str]:
    async with db.execute("SELECT * FROM passwords") as cursor:
        return [record[0] for record in await cursor.fetchall()]


async def login(
        db: Connection,
        key: str,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(db, key, label, "login", value)


async def email(
        db: Connection,
        key: str,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(db, key, label, "email", value)


async def phone(
        db: Connection,
        key: str,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(db, key, label, "phone", value)


async def password(
        db: Connection,
        key: str,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(db, key, label, "password", value)


async def url(
        db: Connection,
        key: str,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(db, key, label, "url", value)


async def totp(
        db: Connection,
        key: str,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(db, key, label, "totp", value)


async def backup_codes(
        db: Connection,
        key: str,
        label: str,
        value: list[str] | str | None = None
) -> list[str] | None:
    if value is None:
        backup_codes: str | None = await _do(db, key, label, "backup_codes")
        if backup_codes:
            return json.loads(backup_codes)
    else:
        if isinstance(value, list):
            value: str = json.dumps(value)
        await _do(db, key, label, "backup_codes", value)
