# import os
# import pytest
# from method import Method
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv('API_KEY')

# method = Method(env='dev', api_key=API_KEY)

# resources = [
#     {"name": "healthcheck", "methods": ["ping"]},
#     # {"name": "accounts", "methods": ["list"]},
#     # {"name": "entities", "methods": ["list"]},
#     # {"name": "payments", "methods": ["list"]},
#     # {"name": "merchants", "methods": ["list"]},
# ]

# # @pytest.mark.parametrize("resource", resources)
# # @pytest.mark.parametrize("method_name", [method for resource in resources for method in resource["methods"]])
# def test_last_response():
#     # resource_name = resource["name"]

#     # if resource_name == "healthcheck":
#     #     response = getattr(method, method_name)()
#     # else:
#     #     response = getattr(getattr(method, resource_name), method_name)()

#     response = method.ping()

#     assert hasattr(response, 'last_response'), "Response should have a 'last_response' attribute"
    
#     last_response = getattr(response, '_last_response')

#     assert hasattr(last_response, 'request_id'), "'last_response' should have 'request_id'"
#     assert hasattr(last_response, 'idempotency_status'), "'last_response' should have 'idempotency_status'"
#     assert hasattr(last_response, 'method'), "'last_response' should have 'method'"
#     assert hasattr(last_response, 'path'), "'last_response' should have 'path'"
#     assert hasattr(last_response, 'status'), "'last_response' should have 'status'"
#     assert hasattr(last_response, 'request_start_time'), "'last_response' should have 'request_start_time'"
#     assert hasattr(last_response, 'request_end_time'), "'last_response' should have 'request_end_time'"
#     assert hasattr(last_response, 'pagination'), "'last_response' should have 'pagination'"

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
    assert hasattr(response, 'last_response'), "Response should have a 'last_response' attribute"
    last_response = getattr(response, '_last_response')
    assert hasattr(last_response, 'request_id'), "'last_response' should have 'request_id'"
