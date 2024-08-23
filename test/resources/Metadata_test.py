import os
import pytest
from dotenv import load_dotenv
from method import Method

@pytest.fixture(scope="module")
def client():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return Method({"api_key": api_key, "env": "dev"})

resources = [
    {"name": "healthcheck", "methods": "ping"},
    {"name": "accounts", "methods": "list"},
    {"name": "entities", "methods": "list"},
    {"name": "payments", "methods": "list"},
    {"name": "merchants", "methods": "list"},
]

@pytest.mark.parametrize("resource", resources)
def test_last_response(client, resource):
    if resource["name"] == "healthcheck":
        response = getattr(client, resource["methods"])()
    else:
        response = getattr(getattr(client, resource["name"]), resource["methods"])()

    assert hasattr(response, 'last_response'), "Response should have a 'last_response' attribute"
    last_response = response.last_response

    assert hasattr(last_response, 'request_id'), "'last_response' should have 'request_id'"
    assert hasattr(last_response, 'idempotency_status'), "'last_response' should have 'idempotency_status'"
    assert hasattr(last_response, 'method'), "'last_response' should have 'method'"
    assert hasattr(last_response, 'path'), "'last_response' should have 'path'"
    assert hasattr(last_response, 'status'), "'last_response' should have 'status'"
    assert hasattr(last_response, 'request_start_time'), "'last_response' should have 'request_start_time'"
    assert hasattr(last_response, 'request_end_time'), "'last_response' should have 'request_end_time'"
    assert hasattr(last_response, 'pagination'), "'last_response' should have 'pagination'"
    assert last_response.request_id, "request_id should not be empty"
    assert last_response.method, "method should not be empty"
    assert last_response.path, "path should not be empty"
    assert last_response.status, "status should not be empty"
    assert last_response.request_start_time is not None, "request_start_time should not be None"
    assert last_response.request_end_time is not None, "request_end_time should not be None"