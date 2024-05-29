import pytest
from method import Method

# Create an instance of Method
method = Method(env='dev', api_key='{API_KEY}')

@pytest.fixture(scope="module")
def setup():
    holder_1_response = method.entities.create({
        'type': 'individual',
        'individual': {
            'first_name': 'Test',
            'last_name': 'McTesterson',
            'phone': '+15121231111'
        }
    })

    method.entities(holder_1_response['id']).verification_sessions.create({
        'type': 'phone',
        'method': 'byo_sms',
        'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z',
        },
    })

    method.entities(holder_1_response['id']).verification_sessions.create({
        'type': 'identity',
        'method': 'kba',
        'kba': {},
    })

    holder_connect_response = method.entities(holder_1_response['id']).connect.create()

    test_credit_card_accounts = method.accounts.list({
        'holder_id': holder_1_response['id'],
        'liability.type': 'credit_card',
        'liability.mch_id': 'mch_302086',
    })
    test_credit_card_account = test_credit_card_accounts[0]

    test_auto_loan_accounts = method.accounts.list({
        'holder_id': holder_1_response['id'],
        'liability.type': 'auto_loan',
        'liability.mch_id': 'mch_2347',
    })
    test_auto_loan_account = test_auto_loan_accounts[0]

    return {
        'holder_1_response': holder_1_response,
        'holder_connect_response': holder_connect_response,
        'test_credit_card_account': test_credit_card_account,
        'test_auto_loan_account': test_auto_loan_account,
    }

def test_create_ach_account(setup):
    holder_1_response = setup['holder_1_response']

    accounts_create_ach_response = method.accounts.create({
        'holder_id': holder_1_response['id'],
        'ach': {
            'routing': '062103000',
            'number': '123456789',
            'type': 'checking',
        },
    })

    expect_results = {
        'id': accounts_create_ach_response['id'],
        'holder_id': holder_1_response['id'],
        'type': 'ach',
        'ach': {
            'routing': '062103000',
            'number': '123456789',
            'type': 'checking',
        },
        'latest_verification_session': accounts_create_ach_response['latest_verification_session'],
        'products': ['payment'],
        'restricted_products': [],
        'status': 'active',
        'error': None,
        'metadata': None,
        'created_at': accounts_create_ach_response['created_at'],
        'updated_at': accounts_create_ach_response['updated_at'],
    }

    assert accounts_create_ach_response == expect_results
