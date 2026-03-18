import pytest
import requests


BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def auth_token(base_url):
    # Generates a fresh token before each test that requires authentication
    payload = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{base_url}/auth", json=payload)
    return response.json()["token"]