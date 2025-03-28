from sqlite3 import IntegrityError, OperationalError

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
