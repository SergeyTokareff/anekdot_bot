import json
import os
from datetime import datetime

USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)


def can_get_joke(user_id: int, chat_id: int) -> bool:
    users = load_users()
    today = datetime.now().strftime("%Y-%m-%d")

    key = f"{user_id}_{chat_id}"

    # якщо користувач ще не отримував сьогодні в цій групі
    if key not in users or users[key] != today:
        users[key] = today
        save_users(users)
        return True

    return False
