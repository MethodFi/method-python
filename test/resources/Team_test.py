import os
import pytest
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

TEAM_EXPECTED_KEYS = ['id', 'parent_id', 'name', 'legal_name', 'ein', 'contacts', 'address', 'status', 'created_at', 'updated_at', 'logo']

CREATE_SKIP_REASON = (
    'POST /teams provisions a new sub-team in the shared dev environment, and teams cannot be '
    'deleted via the public API.'
)

ENCRYPTION_KEY_SKIP_REASON = (
    'POST /teams/default_encryption_key replaces the dev team\'s active default encryption key, '
    'mutating shared dev state for every consumer of the team.'
)


def test_list_teams():
    teams_list_response = method.teams.list()

    assert isinstance(teams_list_response.to_dict(), list)

    for team in teams_list_response:
        for key in TEAM_EXPECTED_KEYS:
            assert key in team


@pytest.mark.skip(reason=CREATE_SKIP_REASON)
def test_create_team():
    team_create_response = method.teams.create({
        'name': 'Test Sub Team',
        'legal_name': 'Test Sub Team LLC',
        'ein': '12-3456789',
        'contacts': [{
            'name': 'Kevin Doyle',
            'email': 'kevin.doyle@gmail.com',
            'type': 'Admin',
        }],
    })

    expect_results = {
        'id': team_create_response['id'],
        'parent_id': team_create_response['parent_id'],
        'name': 'Test Sub Team',
        'legal_name': 'Test Sub Team LLC',
        'ein': '12-3456789',
        'contacts': [{
            'name': 'Kevin Doyle',
            'email': 'kevin.doyle@gmail.com',
            'type': 'Admin',
        }],
        'address': team_create_response['address'],
        'status': team_create_response['status'],
        'logo': team_create_response['logo'],
        'created_at': team_create_response['created_at'],
        'updated_at': team_create_response['updated_at'],
    }

    assert team_create_response == expect_results


@pytest.mark.skip(reason=ENCRYPTION_KEY_SKIP_REASON)
def test_update_encryption_key():
    update_encryption_key_response = method.teams.update_encryption_key({
        'encryption_key': {
            'certificate': '-----BEGIN CERTIFICATE-----\nMIIB...\n-----END CERTIFICATE-----',
        },
    })

    assert update_encryption_key_response.to_dict() is None
