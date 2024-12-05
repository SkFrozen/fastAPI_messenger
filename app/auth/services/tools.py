import re

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from app.settings import settings

key = settings.secret_key[:16].encode("utf-8")
aes = AES.new(key, AES.MODE_ECB)


def encrypt_password(password: str) -> bytes:
    """Encrypt password using AES"""
    password = password.encode("utf-8")
    padded_password = pad(password, AES.block_size)

    encrypted_password = aes.encrypt(padded_password)
    return encrypted_password.hex()


def check_password(password: str, encrypted_password: str) -> bool:
    """Check password using AES"""
    return encrypted_password == encrypt_password(password)


def check_email(email):
    """Check email format"""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}?"
    return bool(re.match(email_regex, email))
