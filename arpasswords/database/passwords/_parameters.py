import json

import keyring
from aiosqlite import Connection

from .. import _base
from ... import crypto


async def _do(
        connection: Connection,
        label: str,
        parameter: str,
        value: str | None = None
) -> str | None:
    if value is None:
        return await _base.get(connection, "passwords", label, parameter)
    await _base.set(connection, "passwords", label, parameter, value)


async def encrypted_password(
        connection: Connection,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(connection, label, "encrypted_password", value)

async def password(
        user_id: int,
        connection: Connection,
        label: str,
        value: str | None = None
) -> str | None:
    key: str = keyring.get_password("keys", str(user_id))
    if value is None:
        encrypted: str = await encrypted_password(connection, label)
        decrypted: str = crypto.decrypt(encrypted, key)
        return decrypted
    encrypted: str = crypto.encrypt(value, key)
    await encrypted_password(connection, label, encrypted)


async def url(
        connection: Connection,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(connection, label, "url", value)


async def encrypted_totp(
        connection: Connection,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(connection, label, "encrypted_totp", value)

async def totp(
        user_id: int,
        connection: Connection,
        label: str,
        value: str | None = None
) -> str | None:
    key: str = keyring.get_password("keys", str(user_id))
    if value is None:
        encrypted: str = await encrypted_totp(connection, label)
        decrypted: str = crypto.decrypt(encrypted, key)
        return decrypted
    encrypted: str = crypto.encrypt(value, key)
    await encrypted_totp(connection, label, encrypted)       


async def encrypted_backup_codes(
        connection: Connection,
        label: str,
        value: str | None = None
) -> str | None:
    return await _do(connection, label, "encrypted_backup_codes", value)


async def backup_codes(
        user_id: int,
        connection: Connection,
        label: str,
        value: list[str] | None = None
) -> list[str] | None:
    key: str = keyring.get_password("keys", str(user_id))
    if value is None:
        encrypted: str = await encrypted_password(connection, label)
        decrypted: str = crypto.decrypt(encrypted, key)
        return json.loads(decrypted)
    encrypted: str = crypto.encrypt(json.dumps(value), key)
    await encrypted_password(connection, label, encrypted)

