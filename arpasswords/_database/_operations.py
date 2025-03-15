from aiosqlite import Connection


async def add(db: Connection, label: str) -> None:
    query: str = "INSERT INTO passwords (label) VALUES (?)"
    await db.execute(query, (label,))


async def delete(db: Connection, label: str) -> None:
    query: str = "DELETE FROM passwords WHERE label = ?"
    await db.execute(query, (label,))
