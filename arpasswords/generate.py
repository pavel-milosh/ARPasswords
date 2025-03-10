import string
import secrets


def password(length: int = 20) -> str:
    power: int = 0
    password: str = ""
    while power < 3:
        password = "".join(
            [
                secrets.choice(string.ascii_letters + string.digits + string.punctuation)
                for _ in range(length)
            ]
        )
        power = (any(letter in password for letter in string.ascii_letters) +
                      any(digit in password for digit in string.digits)+
                      any(char in password for char in string.punctuation))

    return password