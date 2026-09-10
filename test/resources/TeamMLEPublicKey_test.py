import os
import uuid
import pytest
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

pytestmark = pytest.mark.skipif(not API_KEY, reason='API_KEY is not set; skipping live dev API tests.')

method = Method(env='dev', api_key=API_KEY)

test_jwk = {
    'kid': str(uuid.uuid4()),
    'kty': 'RSA',
    'alg': 'RSA-OAEP-256',
    'use': 'enc',
    'n': 'x9hKPiAZKzHhAZx670NMvnvI0ZaEa1I92XsQklLORGVqqECy3oA7In8tkb0FEI2V2yJMZhMkf-4EbsTPZu_D7Hqo3E6fHR0FNd0gocpEy5fBf5at6o92ueVmYiDiXsgxFHZzhEo40a26diRBkzzxYpjxZNtvheQiM34n25kSqvJ3sacIguQs4erqgWl2YR8l1HYIX5_9n3wQ3cuU4a0fcHoLtVmD4fymZ1kiESUiU6qkw-XkYn0BZD3TwTbStQrkXDoFt9D7L7-PLCU5Nmqval5RtI2i4q_uks8t9Hg9YjrM3_FnulT18YiLJ0aGUTgx-qaNoJy5OLGfIg0cfhFrvQ',
    'e': 'AQAB'
}

public_keys_create_response = None
public_keys_retrieve_response = None
public_keys_list_response = None
public_keys_delete_response = None

def test_create_mle_public_key():
    global public_keys_create_response

    public_keys_create_response = method.teams.mle.public_keys.create({
        'type': 'direct',
        'contact': 'engineering@methodfi.com',
        'jwk': test_jwk
    })

    expect_results = {
        'id': public_keys_create_response['id'],
        'type': 'direct',
        'jwk': public_keys_create_response['jwk'],
        'well_known_endpoint': None,
        'status': 'active',
        'contact': 'engineering@methodfi.com',
        'created_at': public_keys_create_response['created_at'],
        'updated_at': public_keys_create_response['updated_at'],
    }

    assert public_keys_create_response == expect_results


def test_list_mle_public_keys():
    global public_keys_list_response

    public_keys_list_response = method.teams.mle.public_keys.list()
    public_key_ids = [public_key['id'] for public_key in public_keys_list_response]

    assert public_keys_create_response['id'] in public_key_ids


def test_retrieve_mle_public_key():
    global public_keys_retrieve_response

    public_keys_retrieve_response = method.teams.mle.public_keys.retrieve(public_keys_create_response['id'])

    expect_results = {
        'id': public_keys_create_response['id'],
        'type': 'direct',
        'jwk': public_keys_retrieve_response['jwk'],
        'well_known_endpoint': None,
        'status': 'active',
        'contact': 'engineering@methodfi.com',
        'created_at': public_keys_retrieve_response['created_at'],
        'updated_at': public_keys_retrieve_response['updated_at'],
    }

    assert public_keys_retrieve_response == expect_results


def test_delete_mle_public_key():
    global public_keys_delete_response

    public_keys_delete_response = method.teams.mle.public_keys.delete(public_keys_create_response['id'])

    assert public_keys_delete_response['status'] == 'disabled'
