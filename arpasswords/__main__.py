import asyncio
import os

from arpasswords import telegram, schedule


async def main() -> None:
    if not os.path.exists("users"):
        os.mkdir("users")
    await schedule.setup()
    await telegram.start()


if __name__ == "__main__":
    asyncio.run(main())