# encryption.py
from cryptography.fernet import Fernet # pyright: ignore[reportMissingImports]
from typing import Union
import os

KEY_FILE = "key.key"

def write_key(filename: str = KEY_FILE) -> None:
    """Generate a new key and save to file (run once)."""
    key = Fernet.generate_key()
    with open(filename, "wb") as f:
        f.write(key)

def load_key(filename: str = KEY_FILE) -> bytes:
    """Load the key from file. Raises FileNotFoundError if missing."""
    with open(filename, "rb") as f:
        return f.read()

def ensure_key(filename: str = KEY_FILE) -> bytes:
    """Make sure a key exists; generate one if not, then return it."""
    if not os.path.exists(filename):
        write_key(filename)
    return load_key(filename)

def encrypt_password(password: str, key: bytes) -> bytes:
    """Return an encrypted token (bytes) for the given password string."""
    f = Fernet(key)
    return f.encrypt(password.encode("utf-8"))

def decrypt_password(encrypted_password: Union[bytes, str], key: bytes) -> str:
    """Return the decrypted plaintext password string."""
    if isinstance(encrypted_password, str):
        encrypted_password = encrypted_password.encode("utf-8")
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode("utf-8")

if __name__ == "__main__":
    # quick test
    key = ensure_key()
    print("Loaded key from:", KEY_FILE)

    original = "MySecretPassword123!"
    print("Original:", original)

    token = encrypt_password(original, key)
    print("Encrypted token:", token)

    recovered = decrypt_password(token, key)
    print("Decrypted:", recovered)

    assert original == recovered
    print("✅ OK: decrypted matches original")
