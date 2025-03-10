import os
import asyncio

from arpasswords import telegram


async def main() -> None:
    if not os.path.exists("users"):
        os.mkdir("users")
    await telegram.start()


if __name__ == "__main__":
    asyncio.run(main())