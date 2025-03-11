from aiosqlite import Connection

from ... import crypto


async def add(db: Connection, key: str,  label: str, password: str) -> None:
    encrypted_password: str = crypto.encrypt(password, key)

    await db.execute(
        "INSERT INTO passwords (label, password) VALUES (?, ?)",
        (label, encrypted_password)
    )
