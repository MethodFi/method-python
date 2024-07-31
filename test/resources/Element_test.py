import os
import pytest
from method import Method
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

element_create_connect_token_response = None

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


def test_create_connect_token(setup):
    global element_create_connect_token_response

    element_create_connect_token_response = method.elements.token.create({
        'entity_id': setup['entity_1_id'],
        'type': 'connect',
        'connect': {
            'products': [ 'balance' ],
            'account_filters': {
                'selection_type': 'multiple',
                'liability_types': [ 'credit_card' ]
            }
        }
    })

    assert 'element_token' in element_create_connect_token_response
    assert len(element_create_connect_token_response) == 1


def test_retrieve_element_results(setup):
    element_retrieve_results_response = method.elements.token.results(element_create_connect_token_response['element_token'])

    expect_results = {
        'authenticated': False,
        'cxn_id': None,
        'accounts': [],
        'entity_id': setup['entity_1_id'],
        'events': []
    }

    assert element_retrieve_results_response == expect_results
