import os
from method import Method
from dotenv import load_dotenv
from method.resources.Teams.Team import Team, MLEPublicKey

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

# A valid RSA public key (JWK) for direct MLE key registration. Method assigns
# the `kid` on registration, so the same material can be re-registered after delete.
TEST_RSA_JWK = {
    'kty': 'RSA',
    'n': (
        '0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4'
        'cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n'
        '3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4Qy'
        'Q5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZ'
        'Hzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6We'
        'Zu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEg'
        'U8awapJzKnqDKgw'
    ),
    'e': 'AQAB',
}

team_retrieve_response = None
team_public_key_create_response = None
team_public_key_retrieve_response = None
team_public_key_list_response = None
team_public_key_delete_response = None


def test_retrieve_team():
    global team_retrieve_response

    team_retrieve_response = method.teams.retrieve()

    team = team_retrieve_response[0]

    expect_results = {
        'id': team['id'],
        'parent_id': team['parent_id'],
        'name': team['name'],
        'legal_name': team['legal_name'],
        'ein': team['ein'],
        'contacts': team['contacts'],
        'address': team['address'],
        'logo': team['logo'],
        'status': team['status'],
        'created_at': team['created_at'],
        'updated_at': team['updated_at'],
    }

    assert team == expect_results


def test_create_team_public_key():
    global team_public_key_create_response

    team_public_key_create_response = method.teams.public_keys.create({
        'type': 'direct',
        'contact': 'mike@methodfi.com',
        'jwk': TEST_RSA_JWK,
    })

    expect_results = {
        'id': team_public_key_create_response['id'],
        'type': team_public_key_create_response['type'],
        'jwk': team_public_key_create_response['jwk'],
        'well_known_endpoint': team_public_key_create_response['well_known_endpoint'],
        'contact': team_public_key_create_response['contact'],
        'status': team_public_key_create_response['status'],
        'created_at': team_public_key_create_response['created_at'],
        'updated_at': team_public_key_create_response['updated_at'],
    }

    assert team_public_key_create_response == expect_results


def test_retrieve_team_public_key():
    global team_public_key_retrieve_response

    team_public_key_retrieve_response = method.teams.public_keys.retrieve(team_public_key_create_response['id'])

    expect_results = {
        'id': team_public_key_create_response['id'],
        'type': team_public_key_retrieve_response['type'],
        'jwk': team_public_key_retrieve_response['jwk'],
        'well_known_endpoint': team_public_key_retrieve_response['well_known_endpoint'],
        'contact': team_public_key_retrieve_response['contact'],
        'status': team_public_key_retrieve_response['status'],
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
