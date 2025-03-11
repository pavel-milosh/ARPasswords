import os
import asyncio

from arpasswords import telegram, _schedule


async def main() -> None:
    if not os.path.exists("users"):
        os.mkdir("users")
    await _schedule.setup()
    await telegram.start()


if __name__ == "__main__":
    asyncio.run(main())