import os
from typing import List
import pytest
import time
from method import Method
from dotenv import load_dotenv 
from utils import await_results
from method.resources.Accounts.Account import Account
from method.resources.Accounts.Balances import AccountBalance
from method.resources.Accounts.CardBrands import AccountCardBrand
from method.resources.Accounts.Payoffs import AccountPayoff
from method.resources.Accounts.Sensitive import AccountSensitive
from method.resources.Accounts.Subscriptions import AccountSubscription, AccountSubscriptionsResponse
from method.resources.Accounts.Transactions import AccountTransaction
from method.resources.Accounts.Updates import AccountUpdate
from method.resources.Accounts.VerificationSessions import AccountVerificationSession
from method.resources.Accounts.Attributes import AccountAttributes
from method.resources.Accounts.Products import AccountProduct, AccountProductListResponse

load_dotenv()
 
API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

accounts_create_ach_response = None
accounts_create_liability_response = None
accounts_retrieve_response = None
accounts_list_response = None
balances_create_response = None
card_brand_create_response = None
payoff_create_response = None
verification_session_create = None
verification_session_update = None
sensitive_data_response = None
transactions_response = None
create_txn_subscriptions_response = None
create_update_subscriptions_response = None
create_update_snapshot_subscriptions_response = None
create_updates_response = None
attributes_create_response = None

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

    phone_verification = method.entities(holder_1_response['id']).verification_sessions.create({
        'type': 'phone',
        'method': 'byo_sms',
        'byo_sms': {
            'timestamp': '2021-09-01T00:00:00.000Z',
        },
    })

    identity_verification = method.entities(holder_1_response['id']).verification_sessions.create({
        'type': 'identity',
        'method': 'kba',
        'kba': {},
    })

    holder_connect_response = method.entities(holder_1_response['id']).connect.create()

    test_credit_card_accounts = method.accounts.list({
        'holder_id': holder_1_response['id'],
        'liability.type': 'credit_card',
        'liability.mch_id': 'mch_302086',
        'status': 'active',
    })
    test_credit_card_account = test_credit_card_accounts[0]

    test_credit_card_accounts_1 = method.accounts.list({
        'holder_id': holder_1_response['id'],
        'liability.type': 'credit_card',
        'liability.mch_id': 'mch_311289',
        'status': 'active',
    })
    test_credit_card_account_1 = test_credit_card_accounts_1[0]

    test_auto_loan_accounts = method.accounts.list({
        'holder_id': holder_1_response['id'],
        'liability.type': 'auto_loan',
        'liability.mch_id': 'mch_311130',
        'status': 'active',
    })
    test_auto_loan_account = test_auto_loan_accounts[0]

    return {
        'holder_1_response': holder_1_response,
        'holder_connect_response': holder_connect_response,
        'test_credit_card_account': test_credit_card_account,
        'test_credit_card_account_1': test_credit_card_account_1,
        'test_auto_loan_account': test_auto_loan_account,
        'phone_verification': phone_verification,
        'identity_verification': identity_verification,
    }


def test_create_ach_account(setup):
    holder_1_response = setup['holder_1_response']
    global accounts_create_ach_response

    accounts_create_ach_response = method.accounts.create({
        'holder_id': holder_1_response['id'],
        'ach': {
            'routing': '062103000',
            'number': '123456789',
            'type': 'checking',
        },
    })

    expect_results: Account = {
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
        'subscriptions': [],
        'available_subscriptions': [],
        'restricted_subscriptions': [],
        'status': 'active',
        'error': None,
        'metadata': None,
        'created_at': accounts_create_ach_response['created_at'],
        'updated_at': accounts_create_ach_response['updated_at'],
    }

    assert accounts_create_ach_response == expect_results


def test_create_liability_account(setup):
    holder_1_response = setup['holder_1_response']
    global accounts_create_liability_response

    accounts_create_liability_response = method.accounts.create({
        'holder_id': holder_1_response['id'],
        'liability': {
            'mch_id': 'mch_302086',
            'account_number': '4936494462408721',
        },
    })

    expect_results: Account = {
        'id': accounts_create_liability_response['id'],
        'holder_id': holder_1_response['id'],
        'type': 'liability',
        'liability': {
            'fingerprint': None,
            'mch_id': 'mch_302086',
            'mask': '8721',
            'ownership': 'unknown',
            'type': 'credit_card',
            'name': 'Chase Sapphire Reserve',
            'sub_type': 'flexible_spending',
        },
        'latest_verification_session': accounts_create_liability_response['latest_verification_session'],
        'balance': None,
        'update': accounts_create_liability_response['update'],
        'attribute': accounts_create_liability_response['attribute'],
        'card_brand': None,
        'payoff': None,
        'products': accounts_create_liability_response['products'],
        'restricted_products': accounts_create_liability_response['restricted_products'],
        'subscriptions': accounts_create_liability_response['subscriptions'],
        'available_subscriptions': [ 'update' ],
        'restricted_subscriptions': [],
        'status': 'active',
        'error': None,
        'metadata': None,
        'created_at': accounts_create_liability_response['created_at'],
        'updated_at': accounts_create_liability_response['updated_at']
    }

    assert accounts_create_liability_response == expect_results


def test_retrieve_account(setup):
    accounts_retrieve_response = method.accounts.retrieve(accounts_create_ach_response['id'])

    expect_results: Account = {
        'id': accounts_create_ach_response['id'],
        'holder_id': setup['holder_1_response']['id'],
        'type': 'ach',
        'ach': {
            'routing': '062103000',
            'number': '123456789',
            'type': 'checking',
        },
        'latest_verification_session': accounts_create_ach_response['latest_verification_session'],
        'products': ['payment'],
        'restricted_products': [],
        'subscriptions': [],
        'available_subscriptions': [],
        'restricted_subscriptions': [],
        'status': 'active',
        'error': None,
        'metadata': None,
        'created_at': accounts_retrieve_response['created_at'],
        'updated_at': accounts_retrieve_response['updated_at'],
    }

    assert accounts_retrieve_response == expect_results


def test_list_accounts(setup):
    holder_1_response = setup['holder_1_response']
    holder_connect_response = setup['holder_connect_response']
    accounts_list_response = method.accounts.list({
        'holder_id': holder_1_response['id'],
        'type': 'liability',
        'status': 'active',
    })

    account_ids = sorted(
        [account['id'] for account in accounts_list_response if account['id'] != accounts_create_liability_response['id']],
        reverse=True
    )[:len(holder_connect_response['accounts']) if holder_connect_response['accounts'] else 0]

    connect_acc_ids = sorted(holder_connect_response['accounts'], reverse=True) if holder_connect_response['accounts'] else ['no_data']
    dupes = account_ids + connect_acc_ids
    test_length = len(set(dupes))

    assert accounts_list_response is not None
    assert isinstance(accounts_list_response._data, list)
    assert test_length == len(connect_acc_ids)


def test_create_balances(setup):
    global balances_create_response
    test_credit_card_account = setup['test_credit_card_account']

    balances_create_response = method.accounts(test_credit_card_account['id']).balances.create()

    expect_results: AccountBalance = {
        'id': balances_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'pending',
        'amount': None,
        'error': None,
        'created_at': balances_create_response['created_at'],
        'updated_at': balances_create_response['updated_at'],
    }

    assert balances_create_response == expect_results


@pytest.mark.asyncio
async def test_retrieve_balance(setup):
    test_credit_card_account = setup['test_credit_card_account']

    def get_account_balances():
        return method.accounts(test_credit_card_account['id']).balances.retrieve(balances_create_response['id'])
    
    balances_retrieve_response = await await_results(get_account_balances)

    expect_results: AccountBalance = {
        'id': balances_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'completed',
        'amount': 1866688,
        'error': None,
        'created_at': balances_retrieve_response['created_at'],
        'updated_at': balances_retrieve_response['updated_at'],
    }

    assert balances_retrieve_response == expect_results


@pytest.mark.asyncio
async def test_list_balances(setup):
    test_credit_card_account = setup['test_credit_card_account']

    def get_balance_list():
        balances = method.accounts(test_credit_card_account['id']).balances.list()
        return balances[0] if balances else None

    balances_list_response_item = await await_results(get_balance_list)

    balances_list_response = method.accounts(test_credit_card_account['id']).balances.list()

    expect_results: AccountBalance = {
        'id': balances_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'completed',
        'amount': 1866688,
        'error': None,
        'created_at': balances_list_response[0]['created_at'],
        'updated_at': balances_list_response[0]['updated_at'],
    }

    assert balances_list_response[0] == expect_results

def test_create_card_brands(setup):
    global card_brand_create_response
    test_credit_card_account = setup['test_credit_card_account']

    card_brand_create_response = method.accounts(test_credit_card_account['id']).card_brands.create()

    expect_results: AccountCardBrand = {
        'id': card_brand_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'in_progress',
        'brands': card_brand_create_response['brands'],
        'shared': False,
        'source': card_brand_create_response['source'],
        'error': None,
        'created_at': card_brand_create_response['created_at'],
        'updated_at': card_brand_create_response['updated_at'],
    }

    time.sleep(5)
    assert card_brand_create_response == expect_results


def test_retrieve_card_brands(setup):
    test_credit_card_account = setup['test_credit_card_account']
    
    card_retrieve_response = method.accounts(test_credit_card_account['id']).card_brands.retrieve(card_brand_create_response['id'])

    expect_results = {
        'id': card_brand_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'completed',
        'shared': False,
        'source': "network",
        'error': None,
        'created_at': card_retrieve_response['created_at'],
        'updated_at': card_retrieve_response['updated_at'],
    }

    for k, v in expect_results.items():
        assert card_retrieve_response[k] == v

    brand = card_retrieve_response['brands'][0]
    assert brand['id'] == 'pdt_15_brd_1'
    assert brand['name'] == 'Chase Sapphire Reserve'
    assert brand['url'] == 'https://static.methodfi.com/card_brands/1b7ccaba6535cb837f802d968add4700.png'
    assert brand['card_product_id'] == 'pdt_15'
    assert brand['type'] == 'specific'
    assert brand['network'] == 'visa'
    assert brand['issuer'] == 'Chase'
    assert brand['description'] == 'Chase Sapphire Reserve'

@pytest.mark.asyncio
async def test_list_card_brands(setup):
    test_credit_card_account = setup['test_credit_card_account']

    card_brands_list_response = method.accounts(test_credit_card_account['id']).card_brands.list()
    result = card_brands_list_response[0]

    assert result['id'] == card_brand_create_response['id']
    assert result['account_id'] == test_credit_card_account['id']
    assert result['status'] == 'completed'
    assert result['shared'] is False
    assert result['source'] == 'network'
    assert result['error'] is None
    assert result['created_at'] == result['created_at']
    assert result['updated_at'] == result['updated_at']

    brand = result['brands'][0]
    assert brand['id'] == 'pdt_15_brd_1'
    assert brand['name'] == 'Chase Sapphire Reserve'
    assert brand['url'] == 'https://static.methodfi.com/card_brands/1b7ccaba6535cb837f802d968add4700.png'
    assert brand['card_product_id'] == 'pdt_15'
    assert brand['type'] == 'specific'
    assert brand['network'] == 'visa'
    assert brand['issuer'] == 'Chase'
    assert brand['description'] == 'Chase Sapphire Reserve'

def test_create_payoffs(setup):
    global payoff_create_response
    test_auto_loan_account = setup['test_auto_loan_account']

    payoff_create_response = method.accounts(test_auto_loan_account['id']).payoffs.create()

    expect_results: AccountPayoff = {
        'id': payoff_create_response['id'],
        'account_id': test_auto_loan_account['id'],
        'amount': None,
        'per_diem_amount': None,
        'term': None,
        'status': 'pending',
        'error': None,
        'created_at': payoff_create_response['created_at'],
        'updated_at': payoff_create_response['updated_at'],
    }

    assert payoff_create_response == expect_results


@pytest.mark.asyncio
async def test_retrieve_payoffs(setup):
    test_auto_loan_account = setup['test_auto_loan_account']
    def get_payoff():
        return method.accounts(test_auto_loan_account['id']).payoffs.retrieve(payoff_create_response['id'])
    
    payoff_retrieve_response = await await_results(get_payoff)

    expect_results: AccountPayoff = {
        'id': payoff_create_response['id'],
        'account_id': test_auto_loan_account['id'],
        'amount': 6083988,
        'per_diem_amount': None,
        'term': 15,
        'status': 'completed',
        'error': None,
        'created_at': payoff_retrieve_response['created_at'],
        'updated_at': payoff_retrieve_response['updated_at'],
    }

    assert payoff_retrieve_response == expect_results

@pytest.mark.asyncio
async def test_list_payoffs(setup):
    test_auto_loan_account = setup['test_auto_loan_account']

    def get_payoff_list():
        payoffs = method.accounts(test_auto_loan_account['id']).payoffs.list()
        return payoffs[0] if payoffs else None

    payoff_list_response_item = await await_results(get_payoff_list)

    payoff_list_response = method.accounts(test_auto_loan_account['id']).payoffs.list()

    expect_results: AccountPayoff = {
        'id': payoff_create_response['id'],
        'account_id': test_auto_loan_account['id'],
        'amount': 6083988,
        'per_diem_amount': None,
        'term': 15,
        'status': 'completed',
        'error': None,
        'created_at': payoff_list_response[0]['created_at'],
        'updated_at': payoff_list_response[0]['updated_at'],
    }

    assert payoff_list_response[0] == expect_results

def test_create_account_verification_sessions(setup):
    global verification_session_create
    test_credit_card_account = setup['test_credit_card_account']

    verification_session_create = method.accounts(test_credit_card_account['id']).verification_sessions.create({
        'type': 'pre_auth'
    })

    expect_results: AccountVerificationSession = {
        'id': verification_session_create['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'pending',
        'type': 'pre_auth',
        'error': None,
        'pre_auth': {
            'billing_zip_code': 'xxxxx',
            'billing_zip_code_check': None,
            'cvv': None,
            'cvv_check': None,
            'exp_check': None,
            'exp_month': 'xx',
            'exp_year': 'xxxx',
            'number': 'xxxxxxxxxxxxxxxx',
            'pre_auth_check': None,
        },
        'created_at': verification_session_create['created_at'],
        'updated_at': verification_session_create['updated_at'],
    }

    assert verification_session_create == expect_results


def test_update_account_verification_sessions(setup):
    global verification_session_update
    test_credit_card_account = setup['test_credit_card_account']

    verification_session_update = method.accounts(test_credit_card_account['id']).verification_sessions.update(verification_session_create['id'], {
        'pre_auth': {
            'exp_month': '03',
            'exp_year': '2028',
            'billing_zip_code': '78758',
            'cvv': '878'
        }
    })

    expect_results: AccountVerificationSession = {
        'id': verification_session_create['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'verified',
        'type': 'pre_auth',
        'error': None,
        'pre_auth': {
            'billing_zip_code': 'xxxxx',
            'billing_zip_code_check': 'pass',
            'cvv': 'xxx',
            'cvv_check': 'pass',
            'exp_check': 'pass',
            'exp_month': 'xx',
            'exp_year': 'xxxx',
            'number': 'xxxxxxxxxxxxxxxx',
            'pre_auth_check': 'pass',
        },
        'created_at': verification_session_update['created_at'],
        'updated_at': verification_session_update['updated_at'],
    }

    assert verification_session_update == expect_results


@pytest.mark.asyncio
async def test_retrieve_account_verification_session(setup):
    test_credit_card_account = setup['test_credit_card_account']
    
    verification_session_retrieve_response = method.accounts(test_credit_card_account['id']).verification_sessions.retrieve(verification_session_update['id'])

    expect_results: AccountVerificationSession = {
        'id': verification_session_update['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'verified',
        'type': 'pre_auth',
        'error': None,
        'pre_auth': {
            'billing_zip_code': 'xxxxx',
            'billing_zip_code_check': 'pass',
            'cvv': 'xxx',
            'cvv_check': 'pass',
            'exp_check': 'pass',
            'exp_month': 'xx',
            'exp_year': 'xxxx',
            'number': 'xxxxxxxxxxxxxxxx',
            'pre_auth_check': 'pass',
        },
        'created_at': verification_session_retrieve_response['created_at'],
        'updated_at': verification_session_retrieve_response['updated_at'],
    }

    assert verification_session_retrieve_response == expect_results

@pytest.mark.asyncio
async def test_list_account_verification_sessions(setup):
    test_credit_card_account = setup['test_credit_card_account']
    
    verification_sessions_list_response = method.accounts(test_credit_card_account['id']).verification_sessions.list()

    expect_results: AccountVerificationSession = {
        'id': verification_session_create['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'verified',
        'type': 'pre_auth',
        'error': None,
        'pre_auth': {
            'billing_zip_code': 'xxxxx',
            'billing_zip_code_check': 'pass',
            'cvv': 'xxx',
            'cvv_check': 'pass',
            'exp_check': 'pass',
            'exp_month': 'xx',
            'exp_year': 'xxxx',
            'number': 'xxxxxxxxxxxxxxxx',
            'pre_auth_check': 'pass',
        },
        'created_at': verification_sessions_list_response[0]['created_at'],
        'updated_at': verification_sessions_list_response[0]['updated_at'],
    }

    assert verification_sessions_list_response[0] == expect_results

def test_create_account_sensitive(setup):
    global sensitive_data_response
    test_credit_card_account = setup['test_credit_card_account']

    sensitive_data_response = method.accounts(test_credit_card_account['id']).sensitive.create({
        'expand': [
            'credit_card.number',
            'credit_card.exp_month',
            'credit_card.exp_year'
        ]
    })

    expect_results: AccountSensitive = {
        'id': sensitive_data_response['id'],
        'account_id': test_credit_card_account['id'],
        'type': 'credit_card',
        'credit_card': {
            'billing_zip_code': None,
            'number': '5555555555551580',
            'exp_month': '03',
            'exp_year': '2028',
            'cvv': None
        },
        'status': 'completed',
        'error': None,
        'created_at': sensitive_data_response['created_at'],
        'updated_at': sensitive_data_response['updated_at']
    }

    assert sensitive_data_response == expect_results


@pytest.mark.asyncio
async def test_list_account_sensitive(setup):
    test_credit_card_account = setup['test_credit_card_account']
    
    sensitive_list_response = method.accounts(test_credit_card_account['id']).sensitive.list()

    expect_results: AccountSensitive = {
        'id': sensitive_data_response['id'],
        'account_id': test_credit_card_account['id'],
        'type': 'credit_card',
        'credit_card': {
            'billing_zip_code': None,
            'number': '5555555555551580',
            'exp_month': '03',
            'exp_year': '2028',
            'cvv': None
        },
        'status': 'completed',
        'error': None,
        'created_at': sensitive_list_response[0]['created_at'],
        'updated_at': sensitive_list_response[0]['updated_at']
    }

    assert sensitive_list_response[0] == expect_results

def test_create_transaction_subscription(setup):
    global create_txn_subscriptions_response
    test_credit_card_account = setup['test_credit_card_account_1']

    network_verification = method.accounts(test_credit_card_account['id']).verification_sessions.create({
        'type': 'network'
    })

    method.accounts(test_credit_card_account['id']).verification_sessions.update(network_verification['id'], {
        'network': {
            'exp_month': '09',
            'exp_year': '2028',
            'billing_zip_code': '78758',
            'cvv': '539'
        }
    })

    create_txn_subscriptions_response = method.accounts(test_credit_card_account['id']).subscriptions.create('transaction')

    expect_results: AccountSubscription = {
        'id': create_txn_subscriptions_response['id'],
        'name': 'transaction',
        'status': 'active',
        'payload': None,
        'latest_request_id': None,
        'created_at': create_txn_subscriptions_response['created_at'],
        'updated_at': create_txn_subscriptions_response['updated_at'],
    }

    assert create_txn_subscriptions_response == expect_results


def test_create_update_subscription(setup):
    global create_update_subscriptions_response
    test_credit_card_account = setup['test_credit_card_account']

    create_update_subscriptions_response = method.accounts(test_credit_card_account['id']).subscriptions.create('update')

    expect_results: AccountSubscription = {
        'id': create_update_subscriptions_response['id'],
        'name': 'update',
        'status': 'active',
        'payload': None,
        'latest_request_id': None,
        'created_at': create_update_subscriptions_response['created_at'],
        'updated_at': create_update_subscriptions_response['updated_at'],
    }

    assert create_update_subscriptions_response == expect_results


def test_create_snapshot_subscription(setup):
    global create_update_snapshot_subscriptions_response
    test_auto_loan_account = setup['test_auto_loan_account']

    create_update_snapshot_subscriptions_response = method.accounts(test_auto_loan_account['id']).subscriptions.create('update.snapshot')

    expect_results: AccountSubscription = {
        'id': create_update_snapshot_subscriptions_response['id'],
        'name': 'update.snapshot',
        'status': 'active',
        'payload': None,
        'latest_request_id': None,
        'created_at': create_update_snapshot_subscriptions_response['created_at'],
        'updated_at': create_update_snapshot_subscriptions_response['updated_at'],
    }

    assert create_update_snapshot_subscriptions_response == expect_results


def test_list_subscriptions(setup):
    test_credit_card_account = setup['test_credit_card_account']
    test_credit_card_account_1 = setup['test_credit_card_account_1']
    test_auto_loan_account = setup['test_auto_loan_account']

    subscriptions_list_response = method.accounts(test_credit_card_account['id']).subscriptions.list()
    subscriptions_transaction_list_response = method.accounts(test_credit_card_account_1['id']).subscriptions.list()
    subscriptions_update_snapshot_list_response = method.accounts(test_auto_loan_account['id']).subscriptions.list()

    expect_results_card: AccountSubscriptionsResponse = {
        'update': {
            'id': create_update_subscriptions_response['id'],
            'name': 'update',
            'status': 'active',
            'payload': None,
            'latest_request_id': None,
            'created_at': create_update_subscriptions_response['created_at'],
            'updated_at': create_update_subscriptions_response['updated_at']
        }
    }

    expect_results_transaction: AccountSubscriptionsResponse = {
        'transaction': {
            'id': create_txn_subscriptions_response['id'],
            'name': 'transaction',
            'status': 'active',
            'payload': None,
            'latest_request_id': None,
            'created_at': create_txn_subscriptions_response['created_at'],
            'updated_at': create_txn_subscriptions_response['updated_at']
        }
    }

    expect_results_auto_loan: AccountSubscriptionsResponse = {
        'update.snapshot': {
            'id': create_update_snapshot_subscriptions_response['id'],
            'name': 'update.snapshot',
            'status': 'active',
            'payload': None,
            'latest_request_id': None,
            'created_at': create_update_snapshot_subscriptions_response['created_at'],
            'updated_at': create_update_snapshot_subscriptions_response['updated_at']
        }
    }

    assert subscriptions_list_response == expect_results_card
    assert subscriptions_transaction_list_response == expect_results_transaction
    assert subscriptions_update_snapshot_list_response == expect_results_auto_loan


def test_retrieve_subscription(setup):
    test_credit_card_account = setup['test_credit_card_account']
    test_credit_card_account_1 = setup['test_credit_card_account_1']
    test_auto_loan_account = setup['test_auto_loan_account']

    retrieve_txn_subscription_response = method.accounts(test_credit_card_account_1['id']).subscriptions.retrieve(create_txn_subscriptions_response['id'])
    retrieve_update_subscription_response = method.accounts(test_credit_card_account['id']).subscriptions.retrieve(create_update_subscriptions_response['id'])
    retrieve_update_snapshot_subscription_response = method.accounts(test_auto_loan_account['id']).subscriptions.retrieve(create_update_snapshot_subscriptions_response['id'])
    
    expect_results_txn: AccountSubscription = {
        'id': create_txn_subscriptions_response['id'],
        'name': 'transaction',
        'status': 'active',
        'payload': None,
        'latest_request_id': None,
        'created_at': retrieve_txn_subscription_response['created_at'],
        'updated_at': retrieve_txn_subscription_response['updated_at'],
    }

    expect_results_update: AccountSubscription = {
        'id': create_update_subscriptions_response['id'],
        'name': 'update',
        'status': 'active',
        'payload': None,
        'latest_request_id': None,
        'created_at': retrieve_update_subscription_response['created_at'],
        'updated_at': retrieve_update_subscription_response['updated_at'],
    }

    expect_results_update_snapshot: AccountSubscription = {
        'id': create_update_snapshot_subscriptions_response['id'],
        'name': 'update.snapshot',
        'status': 'active',
        'payload': None,
        'latest_request_id': None,
        'created_at': retrieve_update_snapshot_subscription_response['created_at'],
        'updated_at': retrieve_update_snapshot_subscription_response['updated_at'],
    }

    assert retrieve_txn_subscription_response == expect_results_txn
    assert retrieve_update_subscription_response == expect_results_update
    assert retrieve_update_snapshot_subscription_response == expect_results_update_snapshot


def test_delete_subscription(setup):
    test_auto_loan_account = setup['test_auto_loan_account']

    delete_update_snapshot_subscription_response = method.accounts(test_auto_loan_account['id']).subscriptions.delete(create_update_snapshot_subscriptions_response['id'])

    expect_results_update_snapshot = {
        'id': create_update_snapshot_subscriptions_response['id'],
        'name': 'update.snapshot',
        'status': 'inactive',
        'payload': None,
        'latest_request_id': None,
        'created_at': delete_update_snapshot_subscription_response['created_at'],
        'updated_at': delete_update_snapshot_subscription_response['updated_at'],
    }

    assert delete_update_snapshot_subscription_response == expect_results_update_snapshot


def test_list_transactions(setup):
    global transactions_response

    test_credit_card_account = setup['test_credit_card_account_1']
    simulated_transaction = method.simulate.accounts(test_credit_card_account['id']).transactions.create()

    transactions_response = method.accounts(test_credit_card_account['id']).transactions.list()

    transactions_response = transactions_response[0]

    expect_results: AccountTransaction = {
        'id': transactions_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'posted',
        'descriptor': simulated_transaction['descriptor'],
        'amount': simulated_transaction['amount'],
        'auth_amount': simulated_transaction['auth_amount'],
        'currency_code': simulated_transaction['currency_code'],
        'transaction_amount': simulated_transaction['transaction_amount'],
        'transaction_auth_amount': simulated_transaction['transaction_auth_amount'],
        'transaction_currency_code': simulated_transaction['transaction_currency_code'],
        'merchant_category_code': simulated_transaction['merchant_category_code'],
        'merchant': simulated_transaction['merchant'],
        'transacted_at': simulated_transaction['transacted_at'],
        'posted_at': simulated_transaction['posted_at'],
        'voided_at': None,
        'original_txn_id': None,
        'created_at': transactions_response['created_at'],
        'updated_at': transactions_response['updated_at'],
    }

    assert transactions_response == expect_results


def test_create_updates(setup):
    global create_updates_response
    test_credit_card_account = setup['test_credit_card_account']

    create_updates_response = method.accounts(test_credit_card_account['id']).updates.create()

    expect_results: AccountUpdate = {
        'id': create_updates_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'pending',
        'source': 'direct',
        'type': 'credit_card',
        'credit_card': {
            'sub_type': None,
            'opened_at': None,
            'closed_at': None,
            'balance': None,
            'last_payment_amount': None,
            'last_payment_date': None,
            'next_payment_due_date': None,
            'next_payment_minimum_amount': None,
            'interest_rate_type': None,
            'interest_rate_percentage_max': None,
            'interest_rate_percentage_min': None,
            'available_credit': None,
            'credit_limit': None,
            'usage_pattern': None
        },
        'data_as_of': create_updates_response['data_as_of'],
        'error': None,
        'created_at': create_updates_response['created_at'],
        'updated_at': create_updates_response['updated_at'],
    }

    assert create_updates_response == expect_results

@pytest.mark.asyncio
async def test_retrieve_updates(setup):
    test_credit_card_account = setup['test_credit_card_account']

    def get_updates():
        return method.accounts(test_credit_card_account['id']).updates.retrieve(create_updates_response['id'])
    
    updates_retrieve_response = await await_results(get_updates)

    expect_results: AccountUpdate = {
        'id': create_updates_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'completed',
        'source': 'direct',
        'type': 'credit_card',
        'credit_card': {
            'sub_type': 'flexible_spending',
            'opened_at': '2016-12-20',
            'closed_at': None,
            'balance': 1866688,
            'last_payment_amount': 100000,
            'last_payment_date': '2023-01-04',
            'next_payment_due_date': '2023-02-09',
            'next_payment_minimum_amount': 51060,
            'interest_rate_type': 'variable',
            'interest_rate_percentage_max': 27.5,
            'interest_rate_percentage_min': 20.5,
            'available_credit': 930000,
            'credit_limit': 2800000,
            'usage_pattern': None
        },
        'data_as_of': updates_retrieve_response['data_as_of'],
        'error': None,
        'created_at': updates_retrieve_response['created_at'],
        'updated_at': updates_retrieve_response['updated_at'],
    }

    assert updates_retrieve_response == expect_results



@pytest.mark.asyncio
async def test_list_updates_for_account(setup):
    test_credit_card_account = setup['test_credit_card_account']

    def get_update_list():
        updates = method.accounts(test_credit_card_account['id']).updates.list()
        return next((update for update in updates if update['id'] == create_updates_response['id']), None)

    update_to_check = await await_results(get_update_list)

    list_updates_response = method.accounts(test_credit_card_account['id']).updates.list()
    update_to_check = next((update for update in list_updates_response if update['id'] == create_updates_response['id']), None)

    expect_results: AccountUpdate = {
        'id': create_updates_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'completed',
        'source': 'direct',
        'type': 'credit_card',
        'credit_card': {
            'sub_type': 'flexible_spending',
            'opened_at': '2016-12-20',
            'closed_at': None,
            'balance': 1866688,
            'last_payment_amount': 100000,
            'last_payment_date': '2023-01-04',
            'next_payment_due_date': '2023-02-09',
            'next_payment_minimum_amount': 51060,
            'interest_rate_type': 'variable',
            'interest_rate_percentage_max': 27.5,
            'interest_rate_percentage_min': 20.5,
            'available_credit': 930000,
            'credit_limit': 2800000,
            'usage_pattern': None
        },
        'data_as_of': update_to_check['data_as_of'] if update_to_check else None,
        'error': None,
        'created_at': update_to_check['created_at'] if update_to_check else None,
        'updated_at': update_to_check['updated_at'] if update_to_check else None
    }


    assert update_to_check == expect_results

def test_create_attributes(setup):
    global attributes_create_response
    test_credit_card_account = setup['test_credit_card_account']

    attributes_create_response = method.accounts(test_credit_card_account['id']).attributes.create()

    expect_results: AccountAttributes = {
        'id': attributes_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'completed',
        'attributes': attributes_create_response['attributes'],
        'error': None,
        'created_at': attributes_create_response['created_at'],
        'updated_at': attributes_create_response['updated_at'],
    }

    assert attributes_create_response == expect_results

def test_list_attributes(setup):
    test_credit_card_account = setup['test_credit_card_account']

    list_attributes_response = method.accounts(test_credit_card_account['id']).attributes.list()

    attribute_to_check = next((attribute for attribute in list_attributes_response if attribute['id'] == attributes_create_response['id']), None)

    expect_results: AccountAttributes = {
        'id': attributes_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'completed',
        'attributes': attributes_create_response['attributes'],
        'error': None,
        'created_at': attribute_to_check['created_at'],
        'updated_at': attribute_to_check['updated_at'],
    }

    assert attribute_to_check == expect_results

def test_retrieve_attributes(setup):
    test_credit_card_account = setup['test_credit_card_account']

    retrieve_attributes_response = method.accounts(test_credit_card_account['id']).attributes.retrieve(attributes_create_response['id'])

    expect_results: AccountAttributes = {
        'id': attributes_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'status': 'completed',
        'attributes': attributes_create_response['attributes'],
        'error': None,
        'created_at': retrieve_attributes_response['created_at'],
        'updated_at': retrieve_attributes_response['updated_at'],
    }

    assert retrieve_attributes_response == expect_results

def test_list_account_products(setup):
    test_credit_card_account = setup['test_credit_card_account']
    
    account_products_list_response = method.accounts(test_credit_card_account['id']).products.list()

    expect_results: AccountProductListResponse = {
        'balance': {
            'name': 'balance',
            'status': 'available',
            'status_error': None,
            'latest_request_id': account_products_list_response.get('balance', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('balance', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': account_products_list_response.get('balance', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('balance', {}).get('updated_at', ''),
        },
        'payment': {
            'name': 'payment',
            'status': 'available',
            'status_error': None,
            'latest_request_id': account_products_list_response.get('payment', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('payment', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': account_products_list_response.get('payment', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('payment', {}).get('updated_at', ''),
        },
        'sensitive': {
            'name': 'sensitive',
            'status': 'available',
            'status_error': None,
            'latest_request_id': account_products_list_response.get('sensitive', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('sensitive', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': account_products_list_response.get('sensitive', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('sensitive', {}).get('updated_at', ''),
        },
        'update': {
            'name': 'update',
            'status': 'available',
            'status_error': None,
            'latest_request_id': account_products_list_response.get('update', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('update', {}).get('latest_successful_request_id', None),
            'is_subscribable': True,
            'created_at': account_products_list_response.get('update', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('update', {}).get('updated_at', ''),
        },
        'attribute': {
            'name': 'attribute',
            'status': 'available',
            'status_error': None,
            'latest_request_id': account_products_list_response.get('attribute', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('attribute', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': account_products_list_response.get('attribute', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('attribute', {}).get('updated_at', ''),
        },
        'transaction': {
            'name': 'transaction',
            'status': 'unavailable',
            'status_error': account_products_list_response.get('transaction', {}).get('status_error', None),
            'latest_request_id': account_products_list_response.get('transaction', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('transaction', {}).get('latest_successful_request_id', None),
            'is_subscribable': True,
            'created_at': account_products_list_response.get('transaction', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('transaction', {}).get('updated_at', ''),
        },
        'payoff': {
            'name': 'payoff',
            'status': 'unavailable',
            'status_error': account_products_list_response.get('payoff', {}).get('status_error', None),
            'latest_request_id': account_products_list_response.get('payoff', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('payoff', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': account_products_list_response.get('payoff', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('payoff', {}).get('updated_at', ''),
        },
        'card_brand': {
            'name': 'card_brand',
            'status': 'available',
            'status_error': None,
            'latest_request_id': account_products_list_response.get('card_brand', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('card_brand', {}).get('latest_successful_request_id', None),
            'is_subscribable': True,
            'created_at': account_products_list_response.get('card_brand', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('card_brand', {}).get('updated_at', ''),
        },
        'payment_instrument.card': {
            'name': 'payment_instrument.card',
            'status': 'restricted',
            'status_error': account_products_list_response.get('payment_instrument.card', {}).get('status_error', None),
            'latest_request_id': account_products_list_response.get('payment_instrument.card', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('payment_instrument.card', {}).get('latest_successful_request_id', None),
            'is_subscribable': True,
            'created_at': account_products_list_response.get('payment_instrument.card', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('payment_instrument.card', {}).get('updated_at', ''),
        },
        'payment_instrument.inbound_achwire_payment': {
            'name': 'payment_instrument.inbound_achwire_payment',
            'status': 'restricted',
            'status_error': account_products_list_response.get('payment_instrument.inbound_achwire_payment', {}).get('status_error', None),
            'latest_request_id': account_products_list_response.get('payment_instrument.inbound_achwire_payment', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('payment_instrument.inbound_achwire_payment', {}).get('latest_successful_request_id', None),
            'is_subscribable': False,
            'created_at': account_products_list_response.get('payment_instrument.inbound_achwire_payment', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('payment_instrument.inbound_achwire_payment', {}).get('updated_at', ''),
        },
        'payment_instrument.network_token': {
            'name': 'payment_instrument.network_token',
            'status': 'restricted',
            'status_error': account_products_list_response.get('payment_instrument.network_token', {}).get('status_error', None),
            'latest_request_id': account_products_list_response.get('payment_instrument.network_token', {}).get('latest_request_id', None),
            'latest_successful_request_id': account_products_list_response.get('payment_instrument.network_token', {}).get('latest_successful_request_id', None),
            'is_subscribable': True,
            'created_at': account_products_list_response.get('payment_instrument.network_token', {}).get('created_at', ''),
            'updated_at': account_products_list_response.get('payment_instrument.network_token', {}).get('updated_at', ''),
        }
    }

    assert account_products_list_response == expect_results

def test_withdraw_account_consent(setup):
    test_credit_card_account = setup['test_credit_card_account']
    holder_1_response = setup['holder_1_response']

    withdraw_consent_response = method.accounts.withdraw_consent(test_credit_card_account['id'])

    expect_results: Account = {
        'id': withdraw_consent_response['id'],
        'holder_id': holder_1_response['id'],
        'status': 'disabled',
        'type': None,
        'liability': None,
        'products': [],
        'restricted_products': [],
        'subscriptions': [],
        'available_subscriptions': [],
        'restricted_subscriptions': [],
        'error': {
            'type': 'ACCOUNT_DISABLED',
            'sub_type': 'ACCOUNT_CONSENT_WITHDRAWN',
            'code': 11004,
            'message': 'Account was disabled due to consent withdrawal.',
        },
        'metadata': None,
        'created_at': withdraw_consent_response['created_at'],
        'updated_at': withdraw_consent_response['updated_at'],
    }

    assert withdraw_consent_response == expect_results