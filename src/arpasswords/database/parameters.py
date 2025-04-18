import json
import logging
from json import JSONDecodeError
from sqlite3 import OperationalError

from aiosqlite import Connection

from . import operations
from .. import crypto, logger
from ..config import _ as config


async def _do(db: Connection, user_id: int, label: str, parameter: str, value: str | None = None) -> str | None:
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
            await logger.user(logging.INFO, user_id, "updated_parameter_value", label=label, parameter=parameter)
    except OperationalError as e:
        if "no such column" in str(e):
            await operations.update_legacy(db, user_id)
            return await _do(db, user_id, label, parameter, value)
        else:
            raise e


async def values(db: Connection, parameter: str, user_id: int = 0) -> list[str]:
    query: str = f"SELECT {parameter} FROM passwords"
    async with db.execute(query) as cursor:
        values: list[str] = []
        for value in await cursor.fetchall():
            if value[0] is None:
                continue
            if parameter == "label":
                values.append(value[0])
            else:
                values.append(await crypto.decrypt(value[0], user_id))
        return values


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


async def additional_parameters(db: Connection, user_id: int, label: str) -> list[str]:
    return [
        additional_parameter
        for additional_parameter in config()["additional_parameters"]
        if await parameter(db, user_id, label, additional_parameter) is not None
    ]
