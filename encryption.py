from cryptography.fernet import Fernet
from typing import Union
import os

KEY_FILE = "key.key"

def write_key(filename: str = KEY_FILE) -> None:
    key = Fernet.generate_key()
    with open(filename, "wb") as f:
        f.write(key)

def load_key(filename: str = KEY_FILE) -> bytes:
    with open(filename, "rb") as f:
        return f.read()

def ensure_key(filename: str = KEY_FILE) -> bytes:
    if not os.path.exists(filename):
        write_key(filename)
    return load_key(filename)

def encrypt_password(password: str, key: bytes) -> str:
    """Return encrypted token as STRING (Base64)."""
    f = Fernet(key)
    return f.encrypt(password.encode("utf-8")).decode("utf-8")

def decrypt_password(token: str, key: bytes) -> str:
    """Decrypt password from string."""
    f = Fernet(key)
    return f.decrypt(token.encode("utf-8")).decode("utf-8")
