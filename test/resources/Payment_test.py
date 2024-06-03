import os
import pytest
from method import Method
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

payments_create_response = None
payments_retrieve_response = None
payments_list_response = None
payments_delete_response = None

@pytest.fixture(scope='module')
def setup():
    holder_1_response = method.entities.create({
        'type': 'individual',
        'individual': {
            'first_name': 'Kevin',
            'last_name': 'Doyle',
            'dob': '1930-03-11',
            'email': 'kevin.doyle@gmail.com',
            'phone': '+15121231111',
        }
    })

    phone_verification_response = method.entities(holder_1_response['id']).verification_sessions.create({
        'type': 'phone',
        'method': 'byo_sms',
        'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z'
        }
    })

    identity_verification_response = method.entities(holder_1_response['id']).verification_sessions.create({
        'type': 'identity',
        'method': 'kba',
        'kba': {}
    })

    source_1_response = method.accounts.create({
        'holder_id': holder_1_response['id'],
        'ach': {
            'routing': '062103000',
            'number': '123456789',
            'type': 'checking',
        }
    })

    destination_1_response = method.accounts.create({
        'holder_id': holder_1_response['id'],
        'liability': {
            'mch_id': 'mch_3',
            'account_number': '123456789',
        }
    })

    return {
        'holder_1_id': holder_1_response['id'],
        'source_1_id': source_1_response['id'],
        'destination_1_id': destination_1_response['id'],
    }


def test_create_payment(setup):
    global payments_create_response

    payments_create_response = method.payments.create({
        'amount': 5000,
        'source': setup['source_1_id'],
        'destination': setup['destination_1_id'],
        'description': 'MethodPy'
    })

    expect_results = {
        'id': payments_create_response['id'],
        'source': setup['source_1_id'],
        'destination': setup['destination_1_id'],
        'amount': 5000,
        'description': 'MethodPy',
        'status': 'pending',
        'estimated_completion_date': payments_create_response['estimated_completion_date'],
        'source_trace_id': None,
        'source_settlement_date': payments_create_response['source_settlement_date'],
        'source_status': 'pending',
        'destination_trace_id': None,
        'destination_settlement_date': payments_create_response['destination_settlement_date'],
        'destination_status': 'pending',
        'reversal_id': None,
        'fee': None,
        'type': 'standard',
        'error': None,
        'metadata': None,
        'created_at': payments_create_response['created_at'],
        'updated_at': payments_create_response['updated_at'],
    }


    assert payments_create_response == expect_results


def test_retrieve_payment(setup):
    global payments_retrieve_response

    payments_retrieve_response = method.payments.retrieve(payments_create_response['id'])

    expect_results = {
        'id': payments_create_response['id'],
        'source': setup['source_1_id'],
        'destination': setup['destination_1_id'],
        'amount': 5000,
        'description': 'MethodPy',
        'status': 'pending',
        'estimated_completion_date': payments_create_response['estimated_completion_date'],
        'source_trace_id': None,
        'source_settlement_date': payments_create_response['source_settlement_date'],
        'source_status': 'pending',
        'destination_trace_id': None,
        'destination_settlement_date': payments_create_response['destination_settlement_date'],
        'destination_status': 'pending',
        'reversal_id': None,
        'fee': None,
        'type': 'standard',
        'error': None,
        'metadata': None,
        'created_at': payments_retrieve_response['created_at'],
        'updated_at': payments_retrieve_response['updated_at'],
        'fund_status': 'pending'
    }

    assert payments_retrieve_response == expect_results


def test_list_payments(setup):
    global payments_list_response

    payments_list_response = method.payments.list({ 'source': setup['source_1_id'] })
    payment_ids = [payment['id'] for payment in payments_list_response]

    assert payments_create_response['id'] in payment_ids


def test_delete_payment(setup):
    global payments_delete_response

    payments_delete_response = method.payments.delete(payments_create_response['id'])

    expect_results = {
        'id': payments_create_response['id'],
        'source': setup['source_1_id'],
        'destination': setup['destination_1_id'],
        'amount': 5000,
        'description': 'MethodPy',
        'status': 'canceled',
        'estimated_completion_date': payments_create_response['estimated_completion_date'],
        'source_trace_id': None,
        'source_settlement_date': payments_create_response['source_settlement_date'],
        'source_status': 'canceled',
        'destination_trace_id': None,
        'destination_settlement_date': payments_create_response['destination_settlement_date'],
        'destination_status': 'canceled',
        'reversal_id': None,
        'fee': None,
        'type': 'standard',
        'error': None,
        'metadata': None,
        'created_at': payments_delete_response['created_at'],
        'updated_at': payments_delete_response['updated_at'],
    }
    
    assert payments_delete_response == expect_results