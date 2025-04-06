import asyncio
from datetime import datetime

from cachetools import TTLCache
from cryptography.fernet import Fernet

from .lang import _ as lang


class Storage:
    def __init__(self) -> None:
        self.time = datetime.now().strftime("%H:%M")
        self.__cipher: Fernet = Fernet(Fernet.generate_key())
        self.__cache: TTLCache = TTLCache(maxsize=1000, ttl=24 * 60 * 60 - 60)


    def delete(self, user_id: int) -> None:
        del self.__cache[user_id]


    def __get(self, user_id: int) -> str:
        return self.__cipher.decrypt(self.__cache[user_id]).decode()


    def __set(self, user_id: int, key: str) -> None:
        self.__cache[user_id] = self.__cipher.encrypt(key.encode())


    async def get(self, user_id: int) -> str | None:
        try:
            return await asyncio.to_thread(self.__get, user_id)
        except KeyError:
            return None


    async def set(self, user_id: int, key: str) -> None:
        return await asyncio.to_thread(self.__set, user_id, key)


    async def reencrypt(self) -> None:
        self.__cache.clear()
        self.__cipher = Fernet(Fernet.generate_key())
        self.__cache = TTLCache(maxsize=1000, ttl=24 * 60 * 60 - 60)
        await lang("main_logger", "storage_reencrypted")


_: Storage = Storage()
