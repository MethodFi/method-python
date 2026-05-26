import os
from method import Method
from dotenv import load_dotenv
from method.resources.Secrets.Secret import Secret

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

secret_create_response = None
secret_retrieve_response = None
secret_list_response = None
secret_delete_response = None


def test_create_secret():
    global secret_create_response

    secret_create_response = method.secrets.create({
        'value': 'test_secret_value',
    })

    expect_results = {
        'id': secret_create_response['id'],
        'metadata': secret_create_response['metadata'],
        'status': 'active',
        'created_at': secret_create_response['created_at'],
        'updated_at': secret_create_response['updated_at'],
    }

    assert secret_create_response == expect_results


def test_retrieve_secret():
    global secret_retrieve_response

    secret_retrieve_response = method.secrets.retrieve(secret_create_response['id'])

    expect_results = {
        'id': secret_create_response['id'],
        'metadata': secret_retrieve_response['metadata'],
        'status': 'active',
        'created_at': secret_retrieve_response['created_at'],
        'updated_at': secret_retrieve_response['updated_at'],
    }

    assert secret_retrieve_response == expect_results


def test_list_secrets():
    global secret_list_response

    secret_list_response = method.secrets.list()

    assert secret_list_response is not None
    assert isinstance(secret_list_response._data, list)


def test_delete_secret():
    global secret_delete_response

    secret_delete_response = method.secrets.delete(secret_create_response['id'])

    assert secret_delete_response is not None
