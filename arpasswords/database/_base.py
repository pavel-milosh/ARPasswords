from aiosqlite import Connection


async def get(
        connection: Connection,
        table: str,
        label: str,
        parameter: str
) -> str | None:
    async with await connection.execute(
            f"SELECT {parameter} FROM {table} WHERE label = ?",
            (label,)
    ) as cursor:
        return await cursor.fetchone()


async def set(
        connection: Connection,
        table: str,
        label: str,
        parameter: str,
        value: str
) -> None:
    await connection.execute(
        f"UPDATE {table} SET {parameter} = ? WHERE label = ?",
        (value, label)
    )