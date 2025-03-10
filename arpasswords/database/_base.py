import os

import aiosqlite
from aiosqlite import Connection


async def create(user_id: int) -> None:
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        await db.execute(
            "CREATE TABLE passwords "
            "("
                "label TEXT NOT NULL PRIMARY KEY,"
                "login TEXT,"
                "email TEXT,"
                "phone TEXT,"
                "password TEXT NOT NULL,"
                "url TEXT,"
                "totp TEXT,"
                "backup_codes TEXT"
            ")"
        )
        await db.commit()


async def get(
        db: Connection,
        table: str,
        label: str,
        parameter: str
) -> str | None:
    async with await db.execute(
            f"SELECT {parameter} FROM {table} WHERE label = ?",
            (label,)
    ) as cursor:
        return (await cursor.fetchone())[0]


async def set(
        db: Connection,
        table: str,
        label: str,
        parameter: str,
        value: str
) -> None:
    await db.execute(
        f"UPDATE {table} SET {parameter} = ? WHERE label = ?",
        (value, label)
    )