import logging
from sqlite3 import IntegrityError, OperationalError

from aiosqlite import Connection

from .exceptions import LabelNotUnique
from .. import logger


async def add(db: Connection, user_id: int, label: str) -> None:
    query: str = "INSERT INTO passwords (label) VALUES (?)"
    try:
        await db.execute(query, (label,))
        await logger.user(logging.INFO, user_id, "added_record", label=label)
    except IntegrityError as e:
        if str(e) == "UNIQUE constraint failed: passwords.label":
            raise LabelNotUnique(user_id, label)
        raise e


async def delete(db: Connection, user_id: int, label: str) -> None:
    query: str = "DELETE FROM passwords WHERE label = ?"
    await db.execute(query, (label,))
    await logger.user(logging.INFO, user_id, "deleted_record", label=label)


async def update_legacy(db: Connection, user_id: int) -> None:
    queries: list[str] = [
        "ALTER TABLE passwords ADD COLUMN backup_codes TEXT",
        "ALTER TABLE passwords ADD COLUMN note TEXT",
        "ALTER TABLE passwords ADD COLUMN pincode TEXT",
        "ALTER TABLE passwords ADD COLUMN site TEXT",
        "ALTER TABLE passwords ADD COLUMN recovery_email TEXT",
        "ALTER TABLE passwords ADD COLUMN previous_password TEXT",
        "ALTER TABLE passwords ADD COLUMN card TEXT",
        "ALTER TABLE passwords DROP COLUMN url"
    ]
    for query in queries:
        try:
            await db.execute(query)
        except OperationalError:
            pass
    await logger.user(logging.INFO, user_id, "updated_legacy_table")
