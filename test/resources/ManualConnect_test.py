import os
import pytest
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

pytestmark = pytest.mark.skipif(not API_KEY, reason='API_KEY is not set; skipping live dev API tests.')

method = Method(env='dev', api_key=API_KEY)

MANUAL_CONNECT_SKIP_REASON = (
    'POST /entities/:ent_id/manual_connect requires a real tradeline payload (a full equifax or '
    'transunion tradeline set with type codes, creditor codes, balances, and payment history) and '
    'an entity provisioned for manual connect; the shared dev environment provides no such fixture.'
)

manual_connect_create_response = None
manual_connect_holder_id = None


@pytest.mark.skip(reason=MANUAL_CONNECT_SKIP_REASON)
def test_create_manual_connect():
    global manual_connect_create_response
    global manual_connect_holder_id

    holder_response = method.entities.create({
        'type': 'individual',
        'individual': {
            'first_name': 'Kevin',
            'last_name': 'Doyle',
            'dob': '1930-03-11',
            'email': 'kevin.doyle@gmail.com',
            'phone': '+15121231111',
        }
    })

    manual_connect_holder_id = holder_response['id']

    manual_connect_create_response = method.entities(manual_connect_holder_id).manual_connect.create({
        'bureau': 'equifax',
        'tradelines': [{
            'type_code': 'CC',
            'portfolio_type_code': 'R',
            'designator_code': 'I',
            'number': '123456XXXX',
            'creditor_name': 'TEST BANK',
            'creditor_code': '999BB99999',
            'balance': 100000,
            'highest_balance': 250000,
            'credit_limit': 500000,
            'term': None,
            'next_payment_minimum_amount': 2500,
            'last_payment_amount': 5000,
            'payment_history': ['1', '1', '1'],
            'past_due_amount': 0,
            'delinquency_charge_off_amount': None,
            'opened_at': '2020-01-01',
            'closed_at': None,
            'last_activity_date': '2024-01-01',
            'reported_date': '2024-01-15',
            'next_payment_due_date': '2024-02-01',
            'last_payment_date': '2024-01-01',
            'delinquency_first_start_date': None,
            'narrative_codes': [{'code': 'AV', 'description': 'AMOUNT IN H/C COLUMN IS CREDIT LIMIT'}],
            'external_id': 'trd_test_1',
        }],
    })

    assert manual_connect_create_response['id'] is not None
    assert manual_connect_create_response['status'] in ['completed', 'in_progress', 'pending', 'failed']


@pytest.mark.skip(reason=MANUAL_CONNECT_SKIP_REASON)
def test_retrieve_manual_connect():
    manual_connect_retrieve_response = method.entities(manual_connect_holder_id).manual_connect.retrieve(
        manual_connect_create_response['id']
    )

    expect_keys = ['id', 'status', 'accounts', 'error', 'created_at', 'updated_at']

    for key in expect_keys:
        assert key in manual_connect_retrieve_response
