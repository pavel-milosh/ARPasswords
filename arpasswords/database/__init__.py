import os

import aiosqlite

from ._operations import add, delete
from ._parameters import parameter, labels


__all__: list[str] = [
    # _operations.py
    "add",
    "delete",
    # _parameters.py
    "labels",
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
                url TEXT,
                totp TEXT
            )
    """
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        await db.execute(query)
        await db.commit()
