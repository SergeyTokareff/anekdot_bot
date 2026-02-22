# import json
# import os
# from datetime import datetime
#
# USERS_FILE = "users.json"
#
#
# def load_users():
#     if not os.path.exists(USERS_FILE):
#         return {}
#     with open(USERS_FILE, "r") as f:
#         return json.load(f)
#
#
# def save_users(data):
#     with open(USERS_FILE, "w") as f:
#         json.dump(data, f)
#
#
# def can_get_joke(user_id: int) -> bool:
#     users = load_users()
#     today = datetime.now().strftime("%Y-%m-%d")
#     user_id = str(user_id)
#
#     if user_id in users and users[user_id] == today:
#         return False
#
#     users[user_id] = today
#     save_users(users)
#     return True
