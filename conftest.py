import pytest

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture
def base_url():
    return BASE_URL