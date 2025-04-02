import asyncio
import os

import aiofiles.os

from arpasswords import logger, schedule, telegram


async def a_main() -> None:
    if not await aiofiles.os.path.exists("users"):
        os.mkdir("users")
    await logger.setup()
    await schedule.setup()
    await telegram.start()


def main() -> None:
    asyncio.run(a_main())


if __name__ == "__main__":
    main()
