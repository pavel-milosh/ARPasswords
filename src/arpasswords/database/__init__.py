import os

import aiosqlite

from . import exceptions
from .operations import add, delete
from .parameters import values, parameter


__all__: list[str] = [
    "exceptions",
    # operations.py
    "add",
    "delete",
    # parameters.py
    "values",
    "parameter"
]


async def create(user_id: int) -> None:
    query: str =\
    """
        CREATE TABLE passwords 
            (
                label TEXT NOT NULL PRIMARY KEY,
                login TEXT,
                email TEXT,
                phone TEXT,
                password TEXT,
                totp TEXT,
                backup_codes TEXT,
                note TEXT
            )
    """
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        await db.execute(query)
        await db.commit()
