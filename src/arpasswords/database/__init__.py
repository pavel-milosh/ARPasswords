import os

import aiosqlite

from . import exceptions
from .operations import add, delete
from .parameters import additional_parameters, parameter, values
from .. import logger


__all__: list[str] = [
    "exceptions",
    # operations.py
    "add",
    "delete",
    # parameters.py
    "additional_parameters",
    "parameter",
    "values"
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
                note TEXT,
                pincode TEXT,
                site TEXT,
                recovery_email TEXT,
                previous_password TEXT,
                card TEXT
            )
    """
    await logger.add_logger(user_id)
    async with aiosqlite.connect(os.path.join("users", f"{user_id}.db")) as db:
        await db.execute(query)
        await db.commit()
