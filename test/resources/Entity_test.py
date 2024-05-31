import os
import pytest
from method import Method
from dotenv import load_dotenv 
from utils import await_results
from method.resources.Entities.Entity import Entity

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