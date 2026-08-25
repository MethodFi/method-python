import os
import pytest
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

pytestmark = pytest.mark.skipif(not API_KEY, reason='API_KEY is not set; skipping live dev API tests.')

method = Method(env='dev', api_key=API_KEY)

secrets_create_response = None
secrets_retrieve_response = None
secrets_list_response = None
secrets_delete_response = None

def test_create_secret():
    global secrets_create_response

    secrets_create_response = method.secrets.create({
        'value': 'test_secret_value'
    })

    expect_results = {
        'id': secrets_create_response['id'],
        'metadata': None,
        'status': 'active',
        'error': None,
        'created_at': secrets_create_response['created_at'],
        'updated_at': secrets_create_response['updated_at'],
    }

    assert secrets_create_response == expect_results


def test_retrieve_secret():
    global secrets_retrieve_response

    secrets_retrieve_response = method.secrets.retrieve(secrets_create_response['id'])

    expect_results = {
        'id': secrets_create_response['id'],
        'metadata': None,
        'status': 'active',
        'error': None,
        'created_at': secrets_retrieve_response['created_at'],
        'updated_at': secrets_retrieve_response['updated_at'],
    }

    assert secrets_retrieve_response == expect_results


def test_list_secrets():
    global secrets_list_response

    secrets_list_response = method.secrets.list()
    secret_ids = [secret['id'] for secret in secrets_list_response]

    assert secrets_create_response['id'] in secret_ids


def test_delete_secret():
    global secrets_delete_response

    secrets_delete_response = method.secrets.delete(secrets_create_response['id'])

    assert secrets_delete_response.to_dict() is None
