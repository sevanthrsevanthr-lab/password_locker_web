import random
import string

def generate_password(length=12):
    """Generate a strong password with uppercase, lowercase, digits, and special characters."""
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+{}[]|:;,.<>?/"

    # Must contain at least 1 of each type
    password = [
        random.choice(upper),
        random.choice(lower),
        random.choice(digits),
        random.choice(symbols)
    ]

    all_chars = upper + lower + digits + symbols
    password += random.choices(all_chars, k=length - 4)

    random.shuffle(password)
    return ''.join(password)
