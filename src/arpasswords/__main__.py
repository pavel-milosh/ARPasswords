import asyncio
import os
import platform
from ctypes import CDLL

import aiofiles.os

from arpasswords import logger, schedule, telegram


async def a_main() -> None:
    if platform.system() == "Linux":
        CDLL("libc.so.6").mlockall(0x0002)
    if not await aiofiles.os.path.exists("users"):
        os.mkdir("users")
    await logger.setup()
    await schedule.setup()
    await telegram.setup()


def main() -> None:
    asyncio.run(a_main())


if __name__ == "__main__":
    main()
