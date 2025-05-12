# --------------------------------------------------------------------------------- #
# ------------ This file is responsible for obtaining the access token ------------ #
# --------------------------------------------------------------------------------- #
from dotenv import load_dotenv
import os
import requests
import json
from pathlib import Path

load_dotenv()
refresh_token = os.getenv("REFRESH_TOKEN")
base_url = os.getenv("BASE_URL")


# This function checks if the Refresh token was obtained successfully from .env
def check_refresh_token():
    if not refresh_token:
        print("Access token is missing or not loaded.")
        return None
    else:
        print(f"Access token loaded: {refresh_token[:5]}...")
        return refresh_token


# This function requests an Access token using the Refresh token
def get_access_token():
    headers = {
        "Bearer": refresh_token,
        "Content-Type": "application/json"
    }

    request_url = f"{base_url}/auth"

    response = requests.post(url=request_url, headers=headers)

    if response.status_code == 201:
        access_token = response.json()["access_token"]
        print(access_token)
        return access_token
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# This function saves the obtained Access token to auth_token.json
def save_access_token(access_token):
    token_data = {
        "access_token": access_token,
    }

    token_path = Path("auth_token.json")

    with token_path.open("w") as f:
        json.dump(token_data, f)

    print("Access token saved to auth_token.json")


# This function loads the Access token from auth_token.json
def load_access_token():
    token_path = Path("auth_token.json")

    if token_path.exists():
        with token_path.open("r") as f:
            token_data = json.load(f)
            return token_data.get("access_token")

    else:
        print("Token file not found.")
        return None


# Main auth function - updates Access token
def update_access_token():
    check_refresh_token()
    token = get_access_token()

    if token:
        save_access_token(token)
    else:
        print("Access token is missing")

