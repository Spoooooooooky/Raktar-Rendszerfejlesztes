import bcrypt
import requests

def hash_password(password: str) -> str:
    """Hash the password locally using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def login(username: str, password: str):
    """Send the hashed password and username to the API for login."""
    hashed_password = hash_password(password)
    response = requests.post(
        "http://127.0.0.1:8000/token",
        data={"username": username, "password": hashed_password},
    )
    if response.status_code == 200:
        print("Login successful! Token:", response.json()["access_token"])
    else:
        print("Login failed!", response.json())

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    login(username, password)