import json

import keyring
from aiosqlite import Connection

from ... import crypto


async def add(
        user_id: int,
        connection: Connection,
        label: str,
        password: str,
        url: str | None = None,
        totp: str | None = None,
        backup_codes: list[str] | None = None
) -> None:
    key: str = keyring.get_password("keys", str(user_id))
    encrypted_password: str = crypto.encrypt(password, key)
    if totp is None:
        encrypted_totp: None = None
    else:
        encrypted_totp: str = crypto.encrypt(password, totp)
    if backup_codes is None:
        encrypted_backup_codes: None = None
    else:
        encrypted_backup_codes: str = crypto.encrypt(
            password,
            json.dumps(backup_codes)
        )
    # noinspection PyTypeChecker
    await connection.execute(
        "INSERT INTO passwords (label, encrypted_password, url, encrypted_totp, encrypted_backup_codes) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            label,
            encrypted_password,
            url,
            encrypted_totp,
            encrypted_backup_codes
        )
    )