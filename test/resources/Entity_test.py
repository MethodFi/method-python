from datetime import datetime, timedelta
import os
from typing import List
from method.resources.Entities.Attributes import EntityAttributes
import pytest
from method import Method
from dotenv import load_dotenv 
from utils import await_results
from method.resources.Entities.Entity import Entity
from method.resources.Entities.Connect import EntityConnect
from method.resources.Entities.CreditScores import EntityCreditScores
from method.resources.Entities.Identities import EntityIdentity
from method.resources.Entities.Products import EntityProduct, EntityProductListResponse
from method.resources.Entities.Subscriptions import EntitySubscription
from method.resources.Entities.VerificationSessions import EntityVerificationSession

load_dotenv()
 
API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

entities_create_response = None
entities_create_async_response = None
entitiy_with_identity_cap = None
entities_retrieve_response = None
entities_update_response = None
entities_update_async_response = None
entities_list_response = None
entities_connect_create_response = None
entities_connect_async_create_response = None
entities_account_list_response = None
entities_account_ids = None
entities_create_credit_score_response = None
entities_create_attribute_response = None
entities_create_idenitity_response = None
entities_create_vehicle_response = None
entity_with_vehicle = None
entities_retrieve_product_list_response = None
entities_create_connect_subscription_response = None
entities_create_credit_score_subscription_response = None
entities_create_attribute_subscription_response = None
entities_create_individual_verification_response = None
entities_create_phone_verification_response = None

# ENTITY CORE METHODS TESTS

def test_create_entity():
    global entities_create_response
    global entities_create_async_response
    entities_create_response = method.entities.create({
        'type': 'individual',
        'individual': {},
        'metadata': {}
    })
    entities_create_async_response = method.entities.create({
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
                    'opal',
                    'kba',
                ],
            },
            'phone': {
                'verified': False,
                'latest_verification_session': None,
                'methods': [
                    'element',
                    'opal',
                    'sna',
                    'sms',
                    'byo_sms',
                ],
            },
          },
          'connect': None,
          'credit_score': None,
          'attribute': None,
          'vehicle': None,
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
                    'opal',
                    'kba'
                ],
            },
            'phone': {
                'verified': False,
                'latest_verification_session': None,
                'methods': [
                    'element',
                    'opal',
                    'sna',
                    'sms',
                    'byo_sms',
                ],
            },
          },
          'connect': None,
          'credit_score': None,
          'attribute': None,
          'vehicle': None,
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
    global entities_update_async_response
    entities_update_response = method.entities.update(entities_create_response['id'], {
        'individual': {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+15121231111'
        }
    })

    entities_update_async_response = method.entities.update(entities_create_async_response['id'], {
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
                    'opal',
                    'kba',
                ],
            },
            'phone': {
                'verified': False,
                'latest_verification_session': entities_update_response['verification']['identity']['latest_verification_session'],
                'methods': [
                    'element',
                    'opal',
                    'sna',
                    'sms',
                    'byo_sms',
                ],
            },
          },
          'connect': None,
          'credit_score': None,
          'attribute': None,
          'vehicle': None,
          'products': [ 'identity' ],
          'restricted_products': entities_update_response['restricted_products'],
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
    # list only those entities created in past hour, in the format of YYYY-MM-DD
    from_date = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d')
    entities_list_response = method.entities.list({'from_date': from_date})
    entities_list_response = [entity['id'] for entity in entities_list_response]

    assert entities_create_response['id'] in entities_list_response

# ENTITY VERIFICATION TESTS

def test_create_entity_phone_verification():
    global entities_create_phone_verification_response
    entities_create_phone_verification_response = method.entities(entities_create_response['id']).verification_sessions.create({
        'type': 'phone',
        'method': 'byo_sms',
        'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z',
        }
    })

    method.entities(entities_create_async_response['id']).verification_sessions.create({
        'type': 'phone',
        'method': 'byo_sms',
        'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z',
        }
    })

    expect_results: EntityVerificationSession = {
        'id': entities_create_phone_verification_response['id'],
        'entity_id': entities_create_response['id'],
        'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z',
        },
        'method': 'byo_sms',
        'status': 'verified',
        'type': 'phone',
        'error': None,
        'created_at': entities_create_phone_verification_response['created_at'],
        'updated_at': entities_create_phone_verification_response['updated_at'],
    }
    
    assert entities_create_phone_verification_response == expect_results


def test_create_entity_individual_verification():
    global entities_create_individual_verification_response
    entities_create_individual_verification_response = method.entities(entities_create_response['id']).verification_sessions.create({
        'type': 'identity',
        'method': 'kba',
        'kba': {}
    })

    method.entities(entities_create_async_response['id']).verification_sessions.create({
        'type': 'identity',
        'method': 'kba',
        'kba': {}
    })

    expect_results: EntityVerificationSession = {
        'id': entities_create_individual_verification_response['id'],
        'entity_id': entities_create_response['id'],
        'kba': {
            'authenticated': True,
            'questions': [],
        },
        'method': 'kba',
        'status': 'verified',
        'type': 'identity',
        'error': None,
        'created_at': entities_create_individual_verification_response['created_at'],
        'updated_at': entities_create_individual_verification_response['updated_at'],
    }
    
    assert entities_create_individual_verification_response == expect_results

async def test_list_entity_verification_sessions():
    verification_sessions_list_response = method.entities(entities_create_response['id']).verification_sessions.list()
    
    # Sort both arrays by type to ensure consistent ordering
    sorted_response = sorted(verification_sessions_list_response, key=lambda x: x['type'])
    sorted_expected = sorted([entities_create_phone_verification_response, entities_create_individual_verification_response], key=lambda x: x['type'])
    
    assert sorted_response == sorted_expected

# ENTITY CONNECT TESTS

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
        'requested_products': [],
        'requested_subscriptions': [],
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
        'requested_products': [],
        'requested_subscriptions': [],
        'error': None,
        'created_at': entities_connect_create_response['created_at'],
        'updated_at': entities_connect_create_response['updated_at'],
    } 
    
    assert entities_connect_retrieve_response == expect_results

async def test_list_entity_connect():
    connect_list_response = method.entities(entities_create_response['id']).connect.list()
    connect_list_response[0]['accounts'] = connect_list_response[0]['accounts'].sort()

    expect_results: EntityConnect = {
        'id': entities_connect_create_response['id'],
        'entity_id': entities_create_response['id'],
        'status': 'completed',
        'accounts': entities_account_ids,
        'requested_products': [],
        'requested_subscriptions': [],
        'error': None,
        'created_at': entities_connect_create_response['created_at'],
        'updated_at': entities_connect_create_response['updated_at'],
    }

    assert connect_list_response[0] == expect_results

def test_create_entity_connect_async():
    global entities_connect_async_create_response
    entities_connect_async_create_response = method.entities(entities_create_async_response['id']).connect.create({
        'products': [ 'update' ],
        'subscriptions': [ 'update' ]
    }, 
    {}, 
    {
        'prefer': 'respond-async'
    })
    entities_connect_async_create_response['accounts'] = entities_connect_async_create_response['accounts'].sort()
    
    expect_results: EntityConnect = {
        'id': entities_connect_async_create_response['id'],
        'entity_id': entities_create_async_response['id'],
        'status': 'pending',
        'accounts': [],
        'requested_products': [ 'update' ],
        'requested_subscriptions': [ 'update' ],
        'error': None,
        'created_at': entities_connect_async_create_response['created_at'],
        'updated_at': entities_connect_async_create_response['updated_at'],
    }

    assert entities_connect_async_create_response == expect_results

@pytest.mark.asyncio
async def test_retrieve_entity_connect_async():
    def get_connect():
        return method.entities(entities_create_async_response['id']).connect.retrieve(entities_connect_async_create_response['id'])
    
    connect_async_retrieve_response = await await_results(get_connect)

    expect_results: EntityConnect = {
        'id': entities_connect_async_create_response['id'],
        'entity_id': entities_create_async_response['id'],
        'status': 'completed',
        'accounts': entities_connect_async_create_response['accounts'],
        'requested_products': [ 'update' ],
        'requested_subscriptions': [ 'update' ],
        'error': None,
        'created_at': entities_connect_async_create_response['created_at'],
        'updated_at': entities_connect_async_create_response['updated_at'],
    }

    assert connect_async_retrieve_response == expect_results

# ENTITY CREDIT SCORE TESTS

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
                'model': 'vantage_4',
                'factors': credit_score_retrieve_response['scores'][0]['factors'],
                'created_at': credit_score_retrieve_response['scores'][0]['created_at']
            }
        ],
        'error': None,
        'created_at': credit_score_retrieve_response['created_at'],
        'updated_at': credit_score_retrieve_response['updated_at']
    }

    assert credit_score_retrieve_response == expect_results


async def test_list_entity_credit_score():
    
    credit_score_list_response = method.entities(entities_create_response['id']).credit_scores.list()

    expect_results: EntityCreditScores = {
        'id': entities_create_credit_score_response['id'],
        'entity_id': entities_create_response['id'],
        'status': 'completed',
        'scores': [
            {
                'score': credit_score_list_response[0]['scores'][0]['score'],
                'source': 'equifax',
                'model': 'vantage_4',
                'factors': credit_score_list_response[0]['scores'][0]['factors'],
                'created_at': credit_score_list_response[0]['scores'][0]['created_at']
            }
        ],
        'error': None,
        'created_at': credit_score_list_response[0]['created_at'],
        'updated_at': credit_score_list_response[0]['updated_at']
    }

    assert credit_score_list_response[0] == expect_results

# ENTITY ATTRIBUTE TESTS

def test_create_entity_attribute():
    global entities_create_attribute_response
    entities_create_attribute_response = method.entities(entities_create_response['id']).attributes.create({
        'attributes': ['credit_health_credit_card_usage']
    })

    expect_results: EntityAttributes = {
        'id': entities_create_attribute_response['id'],
        'entity_id': entities_create_response['id'],
        'status': 'completed',
        'attributes': entities_create_attribute_response['attributes'],
        'error': None,
        'created_at': entities_create_attribute_response['created_at'],
        'updated_at': entities_create_attribute_response['updated_at']
    }

    assert entities_create_attribute_response == expect_results

@pytest.mark.asyncio
async def test_retrieve_entity_attribute():
    def get_attribute():
        return method.entities(entities_create_response['id']).attributes.retrieve(entities_create_attribute_response['id'])
    
    attribute_retrieve_response = await await_results(get_attribute)

    expect_results: EntityAttributes = {
        'id': attribute_retrieve_response['id'],
        'entity_id': entities_create_response['id'],
        'status': 'completed',
        'attributes': attribute_retrieve_response['attributes'],
        'error': None,
        'created_at': attribute_retrieve_response['created_at'],
        'updated_at': attribute_retrieve_response['updated_at']
    }

    assert attribute_retrieve_response == expect_results

async def test_list_entity_attribute():

    attribute_list_response = method.entities(entities_create_response['id']).attributes.list()

    expect_results: EntityAttributes = {
        'id': attribute_list_response[0]['id'],
        'entity_id': entities_create_response['id'],
        'status': 'completed',
        'attributes': attribute_list_response[0]['attributes'],
        'error': None,
        'created_at': attribute_list_response[0]['created_at'],
        'updated_at': attribute_list_response[0]['updated_at']
    }

    assert attribute_list_response[0] == expect_results

# ENTITY IDENTITY TESTS

def test_create_entity_identity():
    global entitiy_with_identity_cap
    global entities_create_idenitity_response

    entitiy_with_identity_cap = method.entities.create({
        'type': 'individual',
        'individual': {
          'first_name': 'Kevin',
          'last_name': 'Doyle',
          'phone': '+16505551115',
        }
    })

    entities_create_idenitity_response = method.entities(entitiy_with_identity_cap['id']).identities.create()

    expect_results: EntityIdentity = {
        'id': entities_create_idenitity_response['id'],
        'entity_id': entitiy_with_identity_cap['id'],
        'status': 'completed',
        'identities': [
          {
            'address': {
              'address': '3300 N INTERSTATE 35',
              'city': 'AUSTIN',
              'postal_code': '78705',
              'state': 'TX'
            },
            'dob': '1997-03-18',
            'first_name': 'KEVIN',
            'last_name': 'DOYLE',
            'phone': '+16505551115',
            'ssn': '111223333'
          },
          {
            'address': {
              'address': '3300 N INTERSTATE 35',
              'city': 'AUSTIN',
              'postal_code': '78705',
              'state': 'TX'
            },
            'dob': '1997-03-18',
            'first_name': 'KEVIN',
            'last_name': 'DOYLE',
            'phone': '+16505551115',
            'ssn': '123456789'
          }
        ],
        'error': None,
        'created_at': entities_create_idenitity_response['created_at'],
        'updated_at': entities_create_idenitity_response['updated_at']
      };

    assert entities_create_idenitity_response == expect_results


@pytest.mark.asyncio
async def test_retrieve_entity_identity():
    def get_identity():
        return method.entities(entitiy_with_identity_cap['id']).identities.retrieve(entities_create_idenitity_response['id'])
    
    identity_retrieve_response = await await_results(get_identity)

    expect_results: EntityIdentity = {
        'id': entities_create_idenitity_response['id'],
        'entity_id': entitiy_with_identity_cap['id'],
        'status': 'completed',
        'identities': [
          {
            'address': {
              'address': '3300 N INTERSTATE 35',
              'city': 'AUSTIN',
              'postal_code': '78705',
              'state': 'TX'
            },
            'dob': '1997-03-18',
            'first_name': 'KEVIN',
            'last_name': 'DOYLE',
            'phone': '+16505551115',
            'ssn': '111223333'
          },
          {
            'address': {
              'address': '3300 N INTERSTATE 35',
              'city': 'AUSTIN',
              'postal_code': '78705',
              'state': 'TX'
            },
            'dob': '1997-03-18',
            'first_name': 'KEVIN',
            'last_name': 'DOYLE',
            'phone': '+16505551115',
            'ssn': '123456789'
          }
        ],
        'error': None,
        'created_at': identity_retrieve_response['created_at'],
        'updated_at': identity_retrieve_response['updated_at']
      };

    assert identity_retrieve_response == expect_results

async def test_list_entity_identity():
    
    identity_list_response = method.entities(entitiy_with_identity_cap['id']).identities.list()

    expect_results: EntityIdentity = {
        'id': entities_create_idenitity_response['id'],
        'entity_id': entitiy_with_identity_cap['id'],
        'status': 'completed',
        'identities': [
          {
            'address': {
              'address': '3300 N INTERSTATE 35',
              'city': 'AUSTIN',
              'postal_code': '78705',
              'state': 'TX'
            },
            'dob': '1997-03-18',
            'first_name': 'KEVIN',
            'last_name': 'DOYLE',
            'phone': '+16505551115',
            'ssn': '111223333'
          },
          {
            'address': {
              'address': '3300 N INTERSTATE 35',
              'city': 'AUSTIN',
              'postal_code': '78705',
              'state': 'TX'
            },
            'dob': '1997-03-18',
            'first_name': 'KEVIN',
            'last_name': 'DOYLE',
            'phone': '+16505551115',
            'ssn': '123456789'
          }
        ],
        'error': None,
        'created_at': identity_list_response[0]['created_at'],
        'updated_at': identity_list_response[0]['updated_at']
      };

    assert identity_list_response[0] == expect_results

# ENTITY VEHICLE TESTS

def test_create_entity_vehicle():
    global entities_create_vehicle_response
    global entity_with_vehicle

    entity_with_vehicle = method.entities.create({
        'type': 'individual',
        'individual': {
          'first_name': 'Kevin',
          'last_name': 'Doyle',
          'phone': '+15121231122',
        }
    })

    method.entities(entity_with_vehicle['id']).verification_sessions.create({
          'type': 'phone',
          'method': 'byo_sms',
          'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z',
        },
    });

    method.entities(entity_with_vehicle['id']).verification_sessions.create({
          'type': 'identity',
          'method': 'kba',
          'kba': {},
    });

    method.entities(entity_with_vehicle['id']).connect.create();

    entities_create_vehicle_response = method.entities(entity_with_vehicle['id']).vehicles.create()

    expect_results: EntityAttributes = {
        'id': entities_create_vehicle_response['id'],
        'entity_id': entity_with_vehicle['id'],
        'status': 'completed',
        'vehicles': entities_create_vehicle_response.vehicles,
        'error': None,
        'created_at': entities_create_vehicle_response['created_at'],
        'updated_at': entities_create_vehicle_response['updated_at']
    }

    assert entities_create_vehicle_response == expect_results

@pytest.mark.asyncio
async def test_retrieve_entity_vehicle():
    def get_vehicle():
        return method.entities(entity_with_vehicle['id']).vehicles.retrieve(entities_create_vehicle_response['id'])
    
    vehicle_retrieve_response = await await_results(get_vehicle)

    expect_results: EntityAttributes = {
        'id': vehicle_retrieve_response['id'],
        'entity_id': entity_with_vehicle['id'],
        'status': 'completed',
        'vehicles': vehicle_retrieve_response.vehicles,
        'error': None,
        'created_at': vehicle_retrieve_response['created_at'],
        'updated_at': vehicle_retrieve_response['updated_at']
    }

    assert vehicle_retrieve_response == expect_results

async def test_list_entity_vehicle():

    vehicle_list_response = method.entities(entity_with_vehicle['id']).vehicles.list()

    expect_results: EntityAttributes = {
        'id': vehicle_list_response[0]['id'],
        'entity_id': entity_with_vehicle['id'],
        'status': 'completed',
        'vehicles': vehicle_list_response[0]['vehicles'],
        'error': None,
        'created_at': vehicle_list_response[0]['created_at'],
        'updated_at': vehicle_list_response[0]['updated_at']
    }

    assert vehicle_list_response[0] == expect_results

# ENTITY PRODUCT TESTS

def test_retrieve_entity_product_list():
    global entities_retrieve_product_list_response
    entities_retrieve_product_list_response = method.entities(entities_create_response['id']).products.list()

    expect_results: EntityProductListResponse = {
        'connect': {
            'name': 'connect',
            'status': 'available',
            'status_error': None,
            'latest_request_id': entities_retrieve_product_list_response.get('connect', {}).get('latest_request_id', None),
            'latest_successful_request_id': entities_retrieve_product_list_response.get('connect', {}).get('latest_successful_request_id', None),
            'is_subscribable': True,
            'created_at': entities_retrieve_product_list_response.get('connect', {}).get('created_at', ''),
            'updated_at': entities_retrieve_product_list_response.get('connect', {}).get('updated_at', ''),
        },
        'credit_score': {
            'name': 'credit_score',
            'status': 'available',
            'status_error': None,
            'latest_request_id': entities_retrieve_product_list_response.get('credit_score', {}).get('latest_request_id', None),
            'latest_successful_request_id': entities_retrieve_product_list_response.get('credit_score', {}).get('latest_successful_request_id', None),
            'is_subscribable': True,
            'created_at': entities_retrieve_product_list_response.get('credit_score', {}).get('created_at', ''),
            'updated_at': entities_retrieve_product_list_response.get('credit_score', {}).get('updated_at', ''),
        },
        'identity': {
            'name': 'identity',
            'status': 'available',
            'status_error': None,
            'latest_request_id': entities_retrieve_product_list_response.get('identity', {}).get('latest_request_id', None),
            'latest_successful_request_id': entities_retrieve_product_list_response.get('identity', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': entities_retrieve_product_list_response.get('identity', {}).get('created_at', ''),
            'updated_at': entities_retrieve_product_list_response.get('identity', {}).get('updated_at', ''),
        },
        'attribute': {
            'name': 'attribute',
            'status': 'available',
            'status_error': None,
            'latest_request_id': entities_retrieve_product_list_response.get('attribute', {}).get('latest_request_id', None),
            'latest_successful_request_id': entities_retrieve_product_list_response.get('attribute', {}).get('latest_successful_request_id', None),
            'is_subscribable': True,
            'created_at': entities_retrieve_product_list_response.get('attribute', {}).get('created_at', ''),
            'updated_at': entities_retrieve_product_list_response.get('attribute', {}).get('updated_at', ''),
        },
        'vehicle': {
            'name': 'vehicle',
            'status': 'available',
            'status_error': None,
            'latest_request_id': entities_retrieve_product_list_response.get('vehicle', {}).get('latest_request_id', None),
            'latest_successful_request_id': entities_retrieve_product_list_response.get('vehicle', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': entities_retrieve_product_list_response.get('vehicle', {}).get('created_at', ''),
            'updated_at': entities_retrieve_product_list_response.get('vehicle', {}).get('updated_at', ''),
        },
        'manual_connect': {
            'name': 'manual_connect',
            'status': 'restricted',
            'status_error': entities_retrieve_product_list_response.get('manual_connect', {}).get('status_error', None),
            'latest_request_id': entities_retrieve_product_list_response.get('manual_connect', {}).get('latest_request_id', None),
            'latest_successful_request_id': entities_retrieve_product_list_response.get('manual_connect', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': entities_retrieve_product_list_response.get('manual_connect', {}).get('created_at', ''),
            'updated_at': entities_retrieve_product_list_response.get('manual_connect', {}).get('updated_at', ''),
        }
    }

    assert entities_retrieve_product_list_response == expect_results

# ENTITY SUBSCRIPTION TESTS

def test_create_entity_connect_subscription():
    global entities_create_connect_subscription_response
    entities_create_connect_subscription_response = method.entities(entities_create_response['id']).subscriptions.create('connect')

    expect_results: EntitySubscription = {
        'id': entities_create_connect_subscription_response['id'],
        'name': 'connect',
        'status': 'active',
        'payload': None,
        'latest_request_id': None,
        'created_at': entities_create_connect_subscription_response['created_at'],
        'updated_at': entities_create_connect_subscription_response['updated_at']
    }

    assert entities_create_connect_subscription_response == expect_results


def test_create_entity_credit_score_subscription():
    global entities_create_credit_score_subscription_response
    entities_create_credit_score_subscription_response = method.entities(entities_create_response['id']).subscriptions.create('credit_score')

    expect_results: EntitySubscription = {
        'id': entities_create_credit_score_subscription_response['id'],
        'name': 'credit_score',
        'status': 'active',
        'payload': None,
        'latest_request_id': None,
        'created_at': entities_create_credit_score_subscription_response['created_at'],
        'updated_at': entities_create_credit_score_subscription_response['updated_at']
    }

    assert entities_create_credit_score_subscription_response == expect_results


def test_create_entity_attribute_subscription():
    global entities_create_attribute_subscription_response
    entities_create_attribute_subscription_response = method.entities(entities_create_response['id']).subscriptions.create({
        'enroll': 'attribute',
        'payload': {
            'attributes': {
                'requested_attributes': ['credit_health_credit_card_usage']
            }
        }
    })

    expect_results: EntitySubscription = {
        'id': entities_create_attribute_subscription_response['id'],
        'name': 'attribute',
        'status': 'active',
        'payload': entities_create_attribute_subscription_response['payload'],
        'latest_request_id': entities_create_attribute_subscription_response['latest_request_id'],
        'created_at': entities_create_attribute_subscription_response['created_at'],
        'updated_at': entities_create_attribute_subscription_response['updated_at']
    }

    assert entities_create_attribute_subscription_response == expect_results


def test_retrieve_entity_subscription():
    entity_connect_subscription_id = entities_create_connect_subscription_response['id']
    entity_credit_score_subscription_id = entities_create_credit_score_subscription_response['id']
    entity_attribute_subscription_id = entities_create_attribute_subscription_response['id']
    entity_connect_subscription_response = method.entities(entities_create_response['id']).subscriptions.retrieve(entity_connect_subscription_id)
    entity_credit_score_subscription_response = method.entities(entities_create_response['id']).subscriptions.retrieve(entity_credit_score_subscription_id)
    entity_attribute_subscription_response = method.entities(entities_create_response['id']).subscriptions.retrieve(entity_attribute_subscription_id)

    expect_connect_results: EntitySubscription = {
        'id': entity_connect_subscription_id,
        'name': 'connect',
        'status': 'active',
        'payload': None,
        'latest_request_id': entity_connect_subscription_response['latest_request_id'],
        'created_at': entity_connect_subscription_response['created_at'],
        'updated_at': entity_connect_subscription_response['updated_at']
    }

    expect_credit_score_results: EntitySubscription = {
        'id': entity_credit_score_subscription_id,
        'name': 'credit_score',
        'status': 'active',
        'payload': None,
        'latest_request_id': entity_credit_score_subscription_response['latest_request_id'],
        'created_at': entity_credit_score_subscription_response['created_at'],
        'updated_at': entity_credit_score_subscription_response['updated_at']
    }

    expect_attribute_results: EntitySubscription = {
        'id': entity_attribute_subscription_id,
        'name': 'attribute',
        'status': 'active',
        'payload': entities_create_attribute_subscription_response['payload'],
        'latest_request_id': entities_create_attribute_subscription_response['latest_request_id'],
        'created_at': entities_create_attribute_subscription_response['created_at'],
        'updated_at': entities_create_attribute_subscription_response['updated_at']
    }

    assert entity_connect_subscription_response == expect_connect_results
    assert entity_credit_score_subscription_response == expect_credit_score_results
    assert entity_attribute_subscription_response == expect_attribute_results
# ENTITY CONSENT TESTS

def test_withdraw_entity_consent():
    entity_withdraw_consent_response = method.entities.withdraw_consent(entities_create_response['id'])

    expect_results: Entity = {
        'id': entities_create_response['id'],
        'type': None,
        'individual': None,
        'verification': None,
        'error': {
            'type': 'ENTITY_DISABLED',
            'sub_type': 'ENTITY_CONSENT_WITHDRAWN',
            'code': 12004,
            'message': 'Entity was disabled due to consent withdrawal.'
        },
        'address': {},
        'status': 'disabled',
        'metadata': None,
        'created_at': entities_update_response['created_at'],
        'updated_at': entity_withdraw_consent_response['updated_at'],
        }
    
    assert entity_withdraw_consent_response == expect_results
    