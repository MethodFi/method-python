import os
from method import Method
from dotenv import load_dotenv
from method.resources.Teams.Team import Team, MLEPublicKey

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

team_retrieve_response = None
team_public_key_create_response = None
team_public_key_retrieve_response = None
team_public_key_list_response = None
team_public_key_delete_response = None


def test_retrieve_team():
    global team_retrieve_response

    team_retrieve_response = method.teams.retrieve()

    expect_results = {
        'id': team_retrieve_response['id'],
        'parent_id': team_retrieve_response['parent_id'],
        'name': team_retrieve_response['name'],
        'legal_name': team_retrieve_response['legal_name'],
        'logo': team_retrieve_response['logo'],
        'api_version': team_retrieve_response['api_version'],
        'status': team_retrieve_response['status'],
        'products': team_retrieve_response['products'],
        'keys': team_retrieve_response['keys'],
        'created_at': team_retrieve_response['created_at'],
        'updated_at': team_retrieve_response['updated_at'],
    }

    assert team_retrieve_response == expect_results


def test_create_team_public_key():
    global team_public_key_create_response

    team_public_key_create_response = method.teams.public_keys.create({
        'jwk': {
            'kty': 'EC',
            'crv': 'P-256',
            'x': 'test_x',
            'y': 'test_y',
        }
    })

    expect_results = {
        'id': team_public_key_create_response['id'],
        'jwk': team_public_key_create_response['jwk'],
        'created_at': team_public_key_create_response['created_at'],
        'updated_at': team_public_key_create_response['updated_at'],
    }

    assert team_public_key_create_response == expect_results


def test_retrieve_team_public_key():
    global team_public_key_retrieve_response

    team_public_key_retrieve_response = method.teams.public_keys.retrieve(team_public_key_create_response['id'])

    expect_results = {
        'id': team_public_key_create_response['id'],
        'jwk': team_public_key_retrieve_response['jwk'],
        'created_at': team_public_key_retrieve_response['created_at'],
        'updated_at': team_public_key_retrieve_response['updated_at'],
    }

    assert team_public_key_retrieve_response == expect_results


def test_list_team_public_keys():
    global team_public_key_list_response

    team_public_key_list_response = method.teams.public_keys.list()

    assert team_public_key_list_response is not None
    assert isinstance(team_public_key_list_response._data, list)


def test_delete_team_public_key():
    global team_public_key_delete_response

    team_public_key_delete_response = method.teams.public_keys.delete(team_public_key_create_response['id'])

    assert team_public_key_delete_response is not None
