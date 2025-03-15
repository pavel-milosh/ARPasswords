import asyncio
import os

from arpasswords import _telegram, _schedule


async def main() -> None:
    if not os.path.exists("users"):
        os.mkdir("users")
    await _schedule.setup()
    await _telegram.start()


if __name__ == "__main__":
    asyncio.run(main())