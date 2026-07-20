import json
import hashlib
import os

DB_FILE = "users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(users, f, indent=4)
        return True
    except Exception:
        return False

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_account(email, password, profile) -> tuple[bool, str]:
    email = email.lower().strip()
    users = load_users()
    if email in users:
        return False, "User already exists with this email address."
    
    users[email] = {
        "password": hash_password(password),
        "profile": profile
    }
    if save_users(users):
        return True, "Account created successfully!"
    return False, "Failed to write user data."

def login(email, password) -> tuple[bool, str, dict]:
    email = email.lower().strip()
    users = load_users()
    if email not in users:
        return False, "User does not exist.", {}
    
    hashed = hash_password(password)
    if users[email]["password"] == hashed:
        profile = users[email].get("profile", {})
        return True, "Login successful!", profile
    return False, "Incorrect password.", {}

def update_profile(email, profile) -> tuple[bool, str]:
    email = email.lower().strip()
    users = load_users()
    if email not in users:
        return False, "User not found."
    
    users[email]["profile"] = profile
    if save_users(users):
        return True, "Profile updated successfully."
    return False, "Failed to update profile."