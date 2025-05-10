# utils/auth.py
import hashlib

# Replace with your actual user database or user list
USER_CREDENTIALS = {
    "a": "e99a18c428cb38d5f260853678922e03",  # password: abc123
    "bob":   "81dc9bdb52d04dc20036dbd8313ed055",  # password: 1234
}

def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def verify_login(username: str, password: str) -> bool:
    hashed = hash_password(password)
    return USER_CREDENTIALS.get(username) == hashed
