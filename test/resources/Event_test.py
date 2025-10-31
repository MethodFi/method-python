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
    attribute_response = method.entities(entity_response['id']).attributes.create({
        'attributes': ['credit_health_credit_card_usage']
    })
    credit_score_response = method.entities(entity_response['id']).credit_scores.create()

    return {
        'entity_response': entity_response,
        'connect_response': connect_response,
        'account_response': account_response,
        'attribute_response': attribute_response,
        'credit_score_response': credit_score_response
    }

def test_simulate_account_opened(setup):
    method.simulate.events.create({
        'type': 'account.opened',
        'entity_id': setup['entity_response']['id']
    })
    
    max_retries = 3
    events_list_response = None
    for _ in range(max_retries):
        sleep(10)  
        events_list_response = method.events.list({
            'type': 'account.opened'
        })
        if events_list_response is not None and len(events_list_response) > 0:
            break
    
    assert events_list_response is not None and len(events_list_response) > 0, "No events returned for 'account.opened'"
    
    event_response = events_list_response[0]
    event_retrieve_response = method.events.retrieve(event_response['id'])

    expect_results = {
        'id': event_response['id'],
        'created_at': event_response['created_at'],
        'updated_at': event_response['updated_at'],
        'type': 'account.opened',
        'resource_id': event_response['resource_id'],
        'resource_type': event_response['resource_type'],
        'data': event_response['data'],
        'diff': event_response['diff']
    }

    assert event_retrieve_response == expect_results