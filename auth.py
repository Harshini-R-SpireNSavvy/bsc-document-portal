import hashlib
import hmac
import json
import os

from dotenv import load_dotenv

load_dotenv()

USERS_FILE = "users.json"


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _load_users() -> dict[str, str]:
    users: dict[str, str] = {}

    default_user = os.getenv("APP_USERNAME", "admin")
    default_pass = os.getenv("APP_PASSWORD", "admin123")
    users[default_user] = _hash_password(default_pass)

    extra = os.getenv("APP_USERS", "")
    for pair in extra.split(","):
        pair = pair.strip()
        if ":" in pair:
            username, password = pair.split(":", 1)
            users[username.strip()] = _hash_password(password.strip())

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, encoding="utf-8") as f:
            users.update(json.load(f))

    return users


_USERS: dict[str, str] | None = None


def get_users() -> dict[str, str]:
    global _USERS
    if _USERS is None:
        _USERS = _load_users()
    return _USERS


def authenticate(username: str, password: str) -> bool:
    users = get_users()
    stored_hash = users.get(username.strip())
    if stored_hash is None:
        return False
    return hmac.compare_digest(stored_hash, _hash_password(password))


def register_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    users = get_users()
    if username in users:
        return False, "Username already exists."

    password_hash = _hash_password(password)
    file_users: dict[str, str] = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, encoding="utf-8") as f:
            file_users = json.load(f)

    file_users[username] = password_hash
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(file_users, f, indent=2)

    global _USERS
    _USERS = None
    return True, "Account created. You can sign in now."


def reload_users() -> None:
    global _USERS
    _USERS = None
