import hashlib

import bcrypt


def hash_password(password: str) -> str:
    """Returns hash of a password"""
    prehashed = hashlib.sha256(password.encode()).hexdigest()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(prehashed.encode(), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Returns true if password correlates to password hash"""
    prehashed = hashlib.sha256(password.encode()).hexdigest()
    return bcrypt.checkpw(prehashed.encode(), hashed_password.encode())
