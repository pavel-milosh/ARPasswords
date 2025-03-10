import keyring
from aiosqlite import Connection

from ... import crypto


async def add(user_id: int, db: Connection, label: str, password: str) -> None:
    key: str = keyring.get_password("keys", str(user_id))
    encrypted_password: str = crypto.encrypt(password, key)

    await db.execute(
        "INSERT INTO passwords (label, password) VALUES (?, ?)",
        (label, encrypted_password)
    )
