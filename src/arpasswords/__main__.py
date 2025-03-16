import asyncio
import os

from arpasswords import telegram, schedule


async def a_main() -> None:
    if not os.path.exists("users"):
        os.mkdir("users")
    await schedule.setup()
    await telegram.start()


def main() -> None:
    asyncio.run(a_main())


if __name__ == "__main__":
    main()
