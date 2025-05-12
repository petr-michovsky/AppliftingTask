# ----------------------------------------------------- #
# ------- This file contains utility functions -------- #
# ----------------------------------------------------- #
from auth import load_access_token, update_access_token
import requests
from dotenv import load_dotenv
import os

load_dotenv()
base_url = os.getenv("BASE_URL")

def register_product(product, retry=True):
    access_token = load_access_token()

    headers = {
        "Bearer": access_token,
        "Content-Type": "application/json"
    }

    request_url = f"{base_url}/products/register"

    product_data = {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
    }

    response = requests.post(url=request_url, headers=headers, json=product_data)
    print(response)

    # Handle case where access token has expired
    if response.status_code == 401 and retry:
        update_access_token()
        return register_product(product, retry=False)

    return response


def get_offers_for_product(product_id, retry=True):
    access_token = load_access_token()

    headers = {
        "Bearer": access_token,
        "Content-Type": "application/json"
    }

    request_url = f"{base_url}/products/{product_id}/offers"

    response = requests.get(url=request_url, headers=headers)

    # Handle case where access token has expired
    if response.status_code == 401 and retry:
        update_access_token()
        return get_offers_for_product(product_id, retry=False)

    return response



