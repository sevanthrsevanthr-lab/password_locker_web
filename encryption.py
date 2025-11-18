from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

KEY_FILE = "key.key"

def write_key(filename: str = KEY_FILE) -> None:
    key = Fernet.generate_key()
    with open(filename, "wb") as f:
        f.write(key)

def load_key(filename: str = KEY_FILE) -> bytes:
    with open(filename, "rb") as f:
        return f.read()

def ensure_key(filename: str = KEY_FILE) -> bytes:
    """
    Load from environment variable first.
    If not found, load key.key file.
    If missing, auto-create key.key
    """
    load_dotenv()
    env_key = os.getenv("SECRET_KEY")

    if env_key:
        return env_key.encode()

    if not os.path.exists(filename):
        write_key(filename)

    return load_key(filename)

def encrypt_password(password: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(token: str, key: bytes) -> str:
    f = Fernet(key)
    try:
        return f.decrypt(token.encode()).decode()
    except:
        return "<error>"
