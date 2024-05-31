import os
import pytest
from method import Method
from dotenv import load_dotenv 
from utils import await_results
from method.resources.Entities.Entity import Entity
from method.resources.Entities.Connect import EntityConnect
from method.resources.Entities.CreditScores import EntityCreditScores
from method.resources.Entities.VerificationSessions import EntityVerificationSession

load_dotenv()
 
API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

entities_create_response = None
entitiy_with_identity_cap = None
entities_retrieve_response = None
entities_update_response = None
entities_list_response = None
entities_connect_create_response = None
entities_account_list_response = None
entities_account_ids = None
entities_create_credit_score_response = None
entities_create_idenitity_response = None
entities_retrieve_product_list_response = None
entities_create_connect_subscription_response = None
entities_create_credit_score_subscription_response = None
entities_create_verification_session_response = None

def test_create_entity():
    global entities_create_response
    entities_create_response = method.entities.create({
        'type': 'individual',
        'individual': {},
        'metadata': {}
    })

    entities_create_response['restricted_subscriptions'] = entities_create_response['restricted_subscriptions'].sort()

    expect_results: Entity = {
        'id': entities_create_response['id'],
        'type': 'individual',
        'individual': {
            'first_name': None,
            'last_name': None,
            'phone': None,
            'dob': None,
            'email': None,
            'ssn': None,
            'ssn_4': None,
        },
        'address': {
            'line1': None,
            'line2': None,
            'city': None,
            'state': None,
            'zip': None,
        },
        'verification': {
            'identity': {
                'verified': False,
                'matched': False,
                'latest_verification_session': None,
                'methods': [
                    'element',
                    'kba',
                ],
            },
            'phone': {
                'verified': False,
                'latest_verification_session': None,
                'methods': [
                    'element',
                    'sna',
                    'sms',
                    'byo_sms'
                ],
            },
          },
          'connect': None,
          'credit_score': None,
          'products': [],
          'restricted_products': entities_create_response['restricted_products'],
          'subscriptions': [],
          'available_subscriptions': [],
          'restricted_subscriptions': [ 'connect', 'credit_score' ].sort(),
          'status': 'incomplete',
          'error': None,
          'metadata': {},
          'created_at': entities_create_response['created_at'],
          'updated_at': entities_create_response['updated_at'],
        }
    
    assert entities_create_response == expect_results

  
def test_retrieve_entity():
    global entities_retrieve_response
    entities_retrieve_response = method.entities.retrieve(entities_create_response['id'])
    entities_retrieve_response['restricted_subscriptions'] = entities_retrieve_response['restricted_subscriptions'].sort()

    expect_results: Entity = {
        'id': entities_create_response['id'],
        'type': 'individual',
        'individual': {
            'first_name': None,
            'last_name': None,
            'phone': None,
            'dob': None,
            'email': None,
            'ssn': None,
            'ssn_4': None,
        },
        'address': {
            'line1': None,
            'line2': None,
            'city': None,
            'state': None,
            'zip': None,
        },
        'verification': {
            'identity': {
                'verified': False,
                'matched': False,
                'latest_verification_session': None,
                'methods': [
                    'element',
                    'kba',
                ],
            },
            'phone': {
                'verified': False,
                'latest_verification_session': None,
                'methods': [
                    'element',
                    'sna',
                    'sms',
                    'byo_sms'
                ],
            },
          },
          'connect': None,
          'credit_score': None,
          'products': [],
          'restricted_products': entities_retrieve_response['restricted_products'],
          'subscriptions': [],
          'available_subscriptions': [],
          'restricted_subscriptions': [ 'connect', 'credit_score' ].sort(),
          'status': 'incomplete',
          'error': None,
          'metadata': {},
          'created_at': entities_retrieve_response['created_at'],
          'updated_at': entities_retrieve_response['updated_at'],
        }
    
    assert entities_retrieve_response == expect_results


def test_update_entity():
    global entities_update_response
    entities_update_response = method.entities.update(entities_create_response['id'], {
        'individual': {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+15121231111'
        }
    })

    entities_update_response['restricted_subscriptions'] = entities_update_response['restricted_subscriptions'].sort()
    entities_update_response['restricted_products'] = entities_update_response['restricted_products'].sort()

    expect_results: Entity = {
        'id': entities_create_response['id'],
        'type': 'individual',
        'individual': {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+15121231111',
            'dob': None,
            'email': None,
            'ssn': None,
            'ssn_4': None,
        },
        'address': {
            'line1': None,
            'line2': None,
            'city': None,
            'state': None,
            'zip': None,
        },
        'verification': {
            'identity': {
                'verified': False,
                'matched': True,
                'latest_verification_session': entities_update_response['verification']['identity']['latest_verification_session'],
                'methods': [
                    'element',
                    'kba',
                ],
            },
            'phone': {
                'verified': False,
                'latest_verification_session': entities_update_response['verification']['identity']['latest_verification_session'],
                'methods': [
                    'element',
                    'sna',
                    'sms',
                    'byo_sms'
                ],
            },
          },
          'connect': None,
          'credit_score': None,
          'products': [ 'identity' ],
          'restricted_products': [ 'connect', 'credit_score' ].sort(),
          'subscriptions': [],
          'available_subscriptions': [],
          'restricted_subscriptions': [ 'connect', 'credit_score' ].sort(),
          'status': 'incomplete',
          'error': None,
          'metadata': {},
          'created_at': entities_update_response['created_at'],
          'updated_at': entities_update_response['updated_at'],
        }
    
    assert entities_update_response == expect_results

def test_list_entities():
    global entities_list_response
    entities_list_response = method.entities.list()
    entities_list_response = [entity['id'] for entity in entities_list_response]

    assert entities_create_response['id'] in entities_list_response


def test_create_entity_phone_verification():
    entity_create_phone_verification_response = method.entities(entities_create_response['id']).verification_sessions.create({
        'type': 'phone',
        'method': 'byo_sms',
        'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z',
        }
    })

    expect_results: EntityVerificationSession = {
        'id': entity_create_phone_verification_response['id'],
        'entity_id': entities_create_response['id'],
        'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z',
        },
        'method': 'byo_sms',
        'status': 'verified',
        'type': 'phone',
        'error': None,
        'created_at': entity_create_phone_verification_response['created_at'],
        'updated_at': entity_create_phone_verification_response['updated_at'],
    }
    
    assert entity_create_phone_verification_response == expect_results


def test_create_entity_individual_verification():
    entity_create_individual_verification_response = method.entities(entities_create_response['id']).verification_sessions.create({
        'type': 'identity',
        'method': 'kba',
        'kba': {}
    })

    expect_results: EntityVerificationSession = {
        'id': entity_create_individual_verification_response['id'],
        'entity_id': entities_create_response['id'],
        'kba': {
            'authenticated': True,
            'questions': [],
        },
        'method': 'kba',
        'status': 'verified',
        'type': 'identity',
        'error': None,
        'created_at': entity_create_individual_verification_response['created_at'],
        'updated_at': entity_create_individual_verification_response['updated_at'],
    }
    
    assert entity_create_individual_verification_response == expect_results


def test_create_entity_connect():
    global entities_connect_create_response
    global entities_account_ids
    entities_connect_create_response = method.entities(entities_create_response['id']).connect.create()
    entities_connect_create_response['accounts'] = entities_connect_create_response['accounts'].sort()
    entities_account_list_response = method.accounts.list({ 'holder_id': entities_create_response['id'], 'type': 'liability' })
    entities_account_ids = [account['id'] for account in entities_account_list_response].sort()
    
    expect_results: EntityConnect = {
        'id': entities_connect_create_response['id'],
        'entity_id': entities_create_response['id'],
        'status': 'completed',
        'accounts': entities_account_ids,
        'error': None,
        'created_at': entities_connect_create_response['created_at'],
        'updated_at': entities_connect_create_response['updated_at'],
    } 
    
    assert entities_connect_create_response == expect_results

def test_retrieve_entity_connect():
    entities_connect_retrieve_response = method.entities(entities_create_response['id']).connect.retrieve(entities_connect_create_response['id'])
    entities_connect_retrieve_response['accounts'] = entities_connect_retrieve_response['accounts'].sort()
    
    expect_results: EntityConnect = {
        'id': entities_connect_create_response['id'],
        'entity_id': entities_create_response['id'],
        'status': 'completed',
        'accounts': entities_account_ids,
        'error': None,
        'created_at': entities_connect_create_response['created_at'],
        'updated_at': entities_connect_create_response['updated_at'],
    } 
    
    assert entities_connect_retrieve_response == expect_results


def test_create_entity_credit_score():
    global entities_create_credit_score_response
    entities_create_credit_score_response = method.entities(entities_create_response['id']).credit_scores.create()
    
    expect_results: EntityCreditScores = {
        'id': entities_create_credit_score_response['id'],
        'entity_id': entities_create_response['id'],
        'status': 'pending',
        'scores': None,
        'error': None,
        'created_at': entities_create_credit_score_response['created_at'],
        'updated_at': entities_create_credit_score_response['updated_at'],
    }
    
    assert entities_create_credit_score_response == expect_results


@pytest.mark.asyncio
async def test_retrieve_entity_credit_score():
    def get_credit_score():
        return method.entities(entities_create_response['id']).credit_scores.retrieve(entities_create_credit_score_response['id'])
    
    credit_score_retrieve_response = await await_results(get_credit_score)

    expect_results: EntityCreditScores = {
        'id': entities_create_credit_score_response['id'],
        'entity_id': entities_create_response['id'],
        'status': 'completed',
        'scores': [
            {
                'score': credit_score_retrieve_response['scores'][0]['score'],
                'source': 'equifax',
                'model': 'vantage_3',
                'factors': credit_score_retrieve_response['scores'][0]['factors'],
                'created_at': credit_score_retrieve_response['scores'][0]['created_at']
            }
        ],
        'error': None,
        'created_at': credit_score_retrieve_response['created_at'],
        'updated_at': credit_score_retrieve_response['updated_at']
    }

    assert credit_score_retrieve_response == expect_results
