import os
import pytest
from method import Method
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

opal_create_identity_verification_token_response = None

@pytest.fixture(scope='module')
def setup():
    entity_1_response = method.entities.create({
        'type': 'individual',
        'individual': {
          'first_name': 'Kevin',
          'last_name': 'Doyle',
          'dob': '1930-03-11',
          'email': 'kevin.doyle@gmail.com',
          'phone': '+15121231111',
        },
    })

    return {
        'entity_1_id': entity_1_response['id'],
    }


def test_create_identity_verification_token(setup):
    global opal_create_identity_verification_token_response

    opal_create_identity_verification_token_response = method.opal.token.create({
        'entity_id': setup['entity_1_id'],
        'mode': 'identity_verification',
        'identity_verification': {
            'skip_pii': ['ssn_4' ]
        }
    })

    assert 'token' in opal_create_identity_verification_token_response
    assert 'valid_until' in opal_create_identity_verification_token_response
    assert 'session_id' in opal_create_identity_verification_token_response
    assert len(opal_create_identity_verification_token_response) == 3
