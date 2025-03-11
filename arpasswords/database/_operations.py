from aiosqlite import Connection


async def add(db: Connection, label: str) -> None:
    query: str = "INSERT INTO passwords (label) VALUES (?)"
    await db.execute(query, (label,))
