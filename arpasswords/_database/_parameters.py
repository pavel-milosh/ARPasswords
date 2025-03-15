import json
from json import JSONDecodeError

from aiosqlite import Connection

from .. import _crypto


async def _do(
        db: Connection,
        key: str,
        label: str,
        parameter: str,
        value: str | None = None
) -> str | None:
    if value is None:
        query: str = f"SELECT {parameter} FROM passwords WHERE label = ?"
        async with await db.execute(query, (label,)) as cursor:
            encrypted: str | None = (await cursor.fetchone())[0]
        if parameter == "label":
            return encrypted
        if encrypted is not None:
            return await _crypto.decrypt(encrypted, key)
    else:
        query: str = f"UPDATE passwords SET {parameter} = ? WHERE label = ?"
        if parameter == "label":
            await db.execute(query, (value, label))
        else:
            await db.execute(query, (await _crypto.encrypt(value, key), label))


async def labels(db: Connection) -> list[str]:
    async with db.execute("SELECT * FROM passwords") as cursor:
        return [record[0] for record in await cursor.fetchall()]


async def parameter(
        db: Connection,
        key: str,
        label: str,
        parameter: str,
        value: str | list[str] | None = None
) -> str | list[str] | None:
    if value is None:
        result: str | None = await _do(db, key, label, parameter, value)
        try:
            return json.loads(result)
        except (JSONDecodeError, TypeError):
            return result
    if isinstance(value, list):
        value = json.dumps(value, ensure_ascii=False)
    await _do(db, key, label, parameter, value)
