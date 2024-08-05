import os
import pytest
from dotenv import load_dotenv
from method import Method

@pytest.fixture(scope="module", autouse=True)
def setup_method():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return Method({"api_key": api_key, "env": "dev"})

def test_method_init(setup_method):
    client = setup_method
    response = client.ping()
    assert response["success"] is True
    assert response["message"] == "pong"
