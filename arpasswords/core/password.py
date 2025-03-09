import string
import random
import os
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes, \
    AEADEncryptionContext, CipherContext
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf: PBKDF2HMAC = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt(password: str, key: str) -> str:
    salt: bytes = os.urandom(16)
    key_256: bytes = _derive_key(key, salt)

    iv: bytes = os.urandom(16)
    cipher: Cipher = Cipher(algorithms.AES(key_256), modes.CBC(iv), backend=default_backend())
    encryptor: AEADEncryptionContext = cipher.encryptor()

    padded_text: bytes = password.encode() + b" " * (16 - len(password) % 16)
    encrypted_bytes: bytes = encryptor.update(padded_text) + encryptor.finalize()

    encrypted_data: str = base64.b64encode(salt + iv + encrypted_bytes).decode()
    return encrypted_data


def decrypt(encrypted_password: str, key: str) -> str:
    encrypted_bytes: bytes = base64.b64decode(encrypted_password)

    salt: bytes = encrypted_bytes[:16]
    iv: bytes = encrypted_bytes[16:32]
    encrypted_text: bytes = encrypted_bytes[32:]

    key_256: bytes = _derive_key(key, salt)
    cipher: Cipher = Cipher(algorithms.AES(key_256), modes.CBC(iv), backend=default_backend())
    decryptor: CipherContext = cipher.decryptor()

    decrypted_text: bytes = decryptor.update(encrypted_text) + decryptor.finalize()
    return decrypted_text.decode().strip()


def generate(
        dictionary: str = string.ascii_letters + string.digits + string.punctuation,
        length: int = 20,
        exclude_chars: str = ""
) -> str:
    for char in exclude_chars:
        dictionary = dictionary.replace(char, "")

    categories: dict[str, str] = {
        "upper": "",
        "lower": "",
        "digit": "",
        "punctuation": ""
    }
    for char in dictionary:
        if char.isupper():
            categories["upper"] += char
        elif char.islower():
            categories["lower"] += char
        elif char.isdigit():
            categories["digit"] += char
        else:
            categories["punctuation"] += char

    while True:
        password: str = ""
        for _ in range(length):
            char: str = random.choice(dictionary)
            password += char
            dictionary = dictionary.replace(char, "")

        for category in categories.values():
            if category and not any(char in password for char in category):
                break
        else:
            break

    return password