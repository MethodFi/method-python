import os
from method import Method
from dotenv import load_dotenv
from method.resources.ForwardingRequests.ForwardingRequest import ForwardingRequest

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

forwarding_request_create_response = None
forwarding_request_retrieve_response = None


def test_create_forwarding_request():
    global forwarding_request_create_response

    forwarding_request_create_response = method.forwarding_requests.create({
        'url': 'https://dev.methodfi.com/accounts',
        'method': 'GET',
        'headers': {},
        'body': '',
        'bindings': {},
    })

    expect_results = {
        'id': forwarding_request_create_response['id'],
        'bindings': forwarding_request_create_response['bindings'],
        'request': forwarding_request_create_response['request'],
        'response': forwarding_request_create_response['response'],
        'duration_ms': forwarding_request_create_response['duration_ms'],
        'status': forwarding_request_create_response['status'],
        'status_history': forwarding_request_create_response['status_history'],
        'created_at': forwarding_request_create_response['created_at'],
    }

    assert forwarding_request_create_response == expect_results


def test_retrieve_forwarding_request():
    global forwarding_request_retrieve_response

    forwarding_request_retrieve_response = method.forwarding_requests.retrieve(forwarding_request_create_response['id'])

    expect_results = {
        'id': forwarding_request_create_response['id'],
        'bindings': forwarding_request_retrieve_response['bindings'],
        'request': forwarding_request_retrieve_response['request'],
        'response': forwarding_request_retrieve_response['response'],
        'duration_ms': forwarding_request_retrieve_response['duration_ms'],
        'status': forwarding_request_retrieve_response['status'],
        'status_history': forwarding_request_retrieve_response['status_history'],
        'created_at': forwarding_request_retrieve_response['created_at'],
    }

    assert forwarding_request_retrieve_response == expect_results
