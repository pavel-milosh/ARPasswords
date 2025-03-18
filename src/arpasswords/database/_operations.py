from sqlite3 import IntegrityError

from aiosqlite import Connection

from .exceptions import LabelNotUnique


async def add(db: Connection, label: str) -> None:
    query: str = "INSERT INTO passwords (label) VALUES (?)"
    try:
        await db.execute(query, (label,))
    except IntegrityError as e:
        if str(e) == "UNIQUE constraint failed: passwords.label":
            raise LabelNotUnique()
        raise e


async def delete(db: Connection, label: str) -> None:
    query: str = "DELETE FROM passwords WHERE label = ?"
    await db.execute(query, (label,))


async def update_legacy(db: Connection) -> None:
    query: str = "ALTER TABLE passwords ADD COLUMN backup_codes TEXT"
    await db.execute(query)
