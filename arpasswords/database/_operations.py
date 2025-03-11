import asyncio

from aiosqlite import Connection

from .. import crypto


async def add(db: Connection, key: str,  label: str, password: str) -> None:
    encrypted_password: str = await crypto.encrypt(password, key)

    query: str = "INSERT INTO passwords (label, password) VALUES (?, ?)"
    await db.execute(query, (label, encrypted_password))
