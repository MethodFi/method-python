from time import sleep
import os
import pytest
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
method = Method(env='dev', api_key=API_KEY)

@pytest.fixture(scope='module')
def setup():
    entity_response = method.entities.create({
        'type': 'individual',
        'individual': {
            'first_name': 'Kevin',
            'last_name': 'Doyle',
            'phone': '+15121231111',
        }
    })

    method.entities(entity_response['id']).verification_sessions.create({
        'type': 'phone',
        'method': 'byo_sms',
        'byo_sms': {
            'timestamp': '2024-03-15T00:00:00.000Z'
        }
    })

    method.entities(entity_response['id']).verification_sessions.create({
        'type': 'identity',
        'method': 'kba',
        'kba': {}
    })

    connect_response = method.entities(entity_response['id']).connect.create()
    account_response = method.accounts.list({'holder_id': entity_response['id']})
    attribute_response = method.entities(entity_response['id']).attributes.create()
    credit_score_response = method.entities(entity_response['id']).credit_scores.create()

    return {
        'entity_response': entity_response,
        'connect_response': connect_response,
        'account_response': account_response,
        'attribute_response': attribute_response,
        'credit_score_response': credit_score_response
    }

def test_simulate_account_closed(setup):
    method.simulate.events.create({
        'type': 'account.closed',
        'account_id': setup['account_response'][0]['id']
    })

    # Wait for event to be created
    sleep(5)

    events_list_response = method.events.list({
        'resource_id': setup['account_response'][0]['id']
    })

    event_response = events_list_response[0]
    event_retrieve_response = method.events.retrieve(event_response['id'])

    expect_results = {
        'id': event_response['id'],
        'created_at': event_response['created_at'],
        'updated_at': event_response['updated_at'],
        'type': 'account.closed',
        'resource_id': setup['account_response'][0]['id'],
        'resource_type': 'account',
        'data': event_response['data'],
        'diff': event_response['diff']
    }

    assert event_retrieve_response == expect_results