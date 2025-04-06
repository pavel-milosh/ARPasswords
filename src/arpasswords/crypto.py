import asyncio
import base64
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .exceptions import Decryption
from .keys import _ as keys


SALT_SIZE: int = 16
NONCE_SIZE: int = 12
KEY_SIZE: int = 32
ITERATIONS: int = 100_000


def _derive_key(key: str, salt: bytes) -> bytes:
    kdf: PBKDF2HMAC = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(key.encode())


def _encrypt(text: str, key: str) -> str:
    salt: bytes = os.urandom(SALT_SIZE)
    nonce: bytes = os.urandom(NONCE_SIZE)
    key_256: bytes = _derive_key(key, salt)
    aesgcm: AESGCM = AESGCM(key_256)
    ciphertext: bytes = aesgcm.encrypt(nonce, text.encode(), None)
    encrypted_data: bytes = salt + nonce + ciphertext
    return base64.b64encode(encrypted_data).decode()


def _decrypt(text: str, key: str) -> str:
    encrypted_bytes: bytes = base64.b64decode(text)
    salt: bytes = encrypted_bytes[:SALT_SIZE]
    nonce: bytes = encrypted_bytes[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext: bytes = encrypted_bytes[SALT_SIZE + NONCE_SIZE:]
    key_256: bytes = _derive_key(key, salt)
    aesgcm: AESGCM = AESGCM(key_256)
    plaintext: bytes = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()


async def encrypt(text: str, user_id: int) -> str:
    return await asyncio.to_thread(_encrypt, text, await keys.get(user_id))


async def decrypt(text: str, user_id: int) -> str:
    try:
        return await asyncio.to_thread(_decrypt, text, await keys.get(user_id))
    except InvalidTag:
        raise Decryption(user_id)
