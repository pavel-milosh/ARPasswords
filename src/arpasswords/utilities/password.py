import asyncio
import secrets
import string


def _generate() -> str:
    password: str = ""
    for _ in range(20):
        password += secrets.choice(string.ascii_letters + string.digits + string.punctuation)

    upper_letters: bool = any(char in password for char in string.ascii_uppercase)
    lower_letters: bool = any(char in password for char in string.ascii_lowercase)
    digits: bool = any(char in password for char in string.digits)
    punctuation: bool = any(char in password for char in string.punctuation)
    if upper_letters + lower_letters + digits + punctuation == 4:
        return password
    return _generate()


async def generate() -> str:
    return await asyncio.to_thread(_generate)
