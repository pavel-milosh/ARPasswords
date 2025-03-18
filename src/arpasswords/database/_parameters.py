import json
from json import JSONDecodeError
from sqlite3 import OperationalError

from aiosqlite import Connection

from . import _operations
from .. import crypto


async def _do(
        db: Connection,
        user_id: int,
        label: str,
        parameter: str,
        value: str | None = None
) -> str | None:
    try:
        if value is None:
            query: str = f"SELECT {parameter} FROM passwords WHERE label = ?"
            async with await db.execute(query, (label,)) as cursor:
                encrypted: str | None = (await cursor.fetchone())[0]
            if parameter == "label":
                return encrypted
            if encrypted is not None:
                return await crypto.decrypt(encrypted, user_id)
        else:
            query: str = f"UPDATE passwords SET {parameter} = ? WHERE label = ?"
            if value.lower() == "none":
                value = None
            elif parameter != "label":
                value = await crypto.encrypt(value, user_id)
            await db.execute(query, (value, label))
    except OperationalError as e:
        if "no such column" in str(e):
            await _operations.update_legacy(db)
            return await _do(db, user_id, label, parameter, value)
        else:
            raise e


async def labels(db: Connection) -> list[str]:
    async with db.execute("SELECT * FROM passwords") as cursor:
        return [record[0] for record in await cursor.fetchall()]


async def parameter(
        db: Connection,
        user_id: int,
        label: str,
        parameter: str,
        value: str | list[str] | None = None
) -> str | list[str] | None:
    if value is None:
        result: str | None = await _do(db, user_id, label, parameter, value)
        try:
            return json.loads(result)
        except (JSONDecodeError, TypeError):
            return result
    if isinstance(value, list):
        value = json.dumps(value, ensure_ascii=False)
    await _do(db, user_id, label, parameter, value)
