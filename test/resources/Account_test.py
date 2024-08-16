import os
import pytest
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

    accounts_create_liability_response['products'] = accounts_create_liability_response['products'].sort()

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
        },
        'latest_verification_session': accounts_create_liability_response['latest_verification_session'],
        'balance': None,
        'update': accounts_create_liability_response['update'],
        'card_brand': None,
        'products': [ 'balance', 'payment', 'sensitive', 'update' ].sort(),
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


def test_create_card_brands(setup):
    global card_brand_create_response
    test_credit_card_account = setup['test_credit_card_account']

    card_brand_create_response = method.accounts(test_credit_card_account['id']).card_brands.create()

    expect_results: AccountCardBrand = {
        'id': card_brand_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'network': 'visa',
        'status': 'completed',
        'issuer': None,
        'last4': '1580',
        'brands': card_brand_create_response['brands'],
        'shared': False,
        'error': None,
        'created_at': card_brand_create_response['created_at'],
        'updated_at': card_brand_create_response['updated_at'],
    }

    assert card_brand_create_response == expect_results


def test_retrieve_card_brands(setup):
    test_credit_card_account = setup['test_credit_card_account']
    card_retrieve_response = method.accounts(test_credit_card_account['id']).card_brands.retrieve(card_brand_create_response['id'])

    expect_results: AccountCardBrand = {
        'id': card_brand_create_response['id'],
        'account_id': test_credit_card_account['id'],
        'network': 'visa',
        'status': 'completed',
        'issuer': None,
        'last4': '1580',
        'brands': card_brand_create_response['brands'],
        'shared': False,
        'error': None,
        'created_at': card_retrieve_response['created_at'],
        'updated_at': card_retrieve_response['updated_at'],
    }

    assert card_retrieve_response == expect_results


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

    def get_verification_session():
        return method.accounts(test_credit_card_account['id']).verification_sessions.retrieve(verification_session_update['id'])
    
    verification_session_retrieve_response = await await_results(get_verification_session)

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


def test_create_transaction_subscription(setup):
    global create_txn_subscriptions_response
    test_credit_card_account = setup['test_credit_card_account']

    create_txn_subscriptions_response = method.accounts(test_credit_card_account['id']).subscriptions.create('transactions')

    expect_results: AccountSubscription = {
        'id': create_txn_subscriptions_response['id'],
        'name': 'transactions',
        'status': 'active',
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
        'latest_request_id': None,
        'created_at': create_update_snapshot_subscriptions_response['created_at'],
        'updated_at': create_update_snapshot_subscriptions_response['updated_at'],
    }

    assert create_update_snapshot_subscriptions_response == expect_results


def test_list_subscriptions(setup):
    test_credit_card_account = setup['test_credit_card_account']
    test_auto_loan_account = setup['test_auto_loan_account']

    subscriptions_list_response = method.accounts(test_credit_card_account['id']).subscriptions.list()
    subscriptions_update_snapshot_list_response = method.accounts(test_auto_loan_account['id']).subscriptions.list()

    expect_results_card: AccountSubscriptionsResponse = {
        'transactions': {
            'id': create_txn_subscriptions_response['id'],
            'name': 'transactions',
            'status': 'active',
            'latest_request_id': None,
            'created_at': create_txn_subscriptions_response['created_at'],
            'updated_at': create_txn_subscriptions_response['updated_at']
        },
        'update': {
            'id': create_update_subscriptions_response['id'],
            'name': 'update',
            'status': 'active',
            'latest_request_id': None,
            'created_at': create_update_subscriptions_response['created_at'],
            'updated_at': create_update_subscriptions_response['updated_at']
        }
    }

    expect_results_auto_loan: AccountSubscriptionsResponse = {
        'update.snapshot': {
            'id': create_update_snapshot_subscriptions_response['id'],
            'name': 'update.snapshot',
            'status': 'active',
            'latest_request_id': None,
            'created_at': create_update_snapshot_subscriptions_response['created_at'],
            'updated_at': create_update_snapshot_subscriptions_response['updated_at']
        }
    }

    assert subscriptions_list_response == expect_results_card
    assert subscriptions_update_snapshot_list_response == expect_results_auto_loan


def test_retrieve_subscription(setup):
    test_credit_card_account = setup['test_credit_card_account']
    test_auto_loan_account = setup['test_auto_loan_account']

    retrieve_txn_subscription_response = method.accounts(test_credit_card_account['id']).subscriptions.retrieve(create_txn_subscriptions_response['id'])
    retrieve_update_subscription_response = method.accounts(test_credit_card_account['id']).subscriptions.retrieve(create_update_subscriptions_response['id'])
    retrieve_update_snapshot_subscription_response = method.accounts(test_auto_loan_account['id']).subscriptions.retrieve(create_update_snapshot_subscriptions_response['id'])
    
    expect_results_txn: AccountSubscription = {
        'id': create_txn_subscriptions_response['id'],
        'name': 'transactions',
        'status': 'active',
        'latest_request_id': None,
        'created_at': retrieve_txn_subscription_response['created_at'],
        'updated_at': retrieve_txn_subscription_response['updated_at'],
    }

    expect_results_update: AccountSubscription = {
        'id': create_update_subscriptions_response['id'],
        'name': 'update',
        'status': 'active',
        'latest_request_id': None,
        'created_at': retrieve_update_subscription_response['created_at'],
        'updated_at': retrieve_update_subscription_response['updated_at'],
    }

    expect_results_update_snapshot: AccountSubscription = {
        'id': create_update_snapshot_subscriptions_response['id'],
        'name': 'update.snapshot',
        'status': 'active',
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
        'latest_request_id': None,
        'created_at': delete_update_snapshot_subscription_response['created_at'],
        'updated_at': delete_update_snapshot_subscription_response['updated_at'],
    }

    assert delete_update_snapshot_subscription_response == expect_results_update_snapshot


def test_list_transactions(setup):
    global transactions_response

    test_credit_card_account = setup['test_credit_card_account']
    simulated_transaction = method.simulate.accounts(test_credit_card_account['id']).transactions.create()

    transactions_response = method.accounts(test_credit_card_account['id']).transactions.list()

    transactions_response = transactions_response[0]

    expect_results: AccountTransaction = {
        'id': transactions_response['id'],
        'account_id': test_credit_card_account['id'],
        'merchant': simulated_transaction['merchant'],
        'network': 'visa',
        'network_data': None,
        'amount': simulated_transaction['amount'],
        'currency': 'USD',
        'billing_amount': simulated_transaction['billing_amount'],
        'billing_currency': 'USD',
        'status': 'cleared',
        'error': None,
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
        'error': None,
        'created_at': updates_retrieve_response['created_at'],
        'updated_at': updates_retrieve_response['updated_at'],
    }

    assert updates_retrieve_response == expect_results



def test_list_updates_for_account(setup):
    test_credit_card_account = setup['test_credit_card_account']

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
        'error': None,
        'created_at': update_to_check['created_at'] if update_to_check else None,
        'updated_at': update_to_check['updated_at'] if update_to_check else None
    }


    assert update_to_check == expect_results


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
