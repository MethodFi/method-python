import os
from method import Method
from dotenv import load_dotenv
from method.resources.ManagedAccounts.ManagedAccount import ManagedAccount, ManagedAccountTransaction

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

managed_account_list_response = None
managed_account_retrieve_response = None
managed_account_transactions_list_response = None


def test_list_managed_accounts():
    global managed_account_list_response

    managed_account_list_response = method.managed_accounts.list()

    assert managed_account_list_response is not None
    assert isinstance(managed_account_list_response._data, list)


def test_retrieve_managed_account():
    global managed_account_retrieve_response

    if not managed_account_list_response._data:
        return

    managed_account_id = managed_account_list_response[0]['id']
    managed_account_retrieve_response = method.managed_accounts.retrieve(managed_account_id)

    expect_results = {
        'id': managed_account_id,
        'type': managed_account_retrieve_response['type'],
        'status': managed_account_retrieve_response['status'],
        'routing_number': managed_account_retrieve_response['routing_number'],
        'account_number': managed_account_retrieve_response['account_number'],
        'balance': managed_account_retrieve_response['balance'],
        'created_at': managed_account_retrieve_response['created_at'],
        'updated_at': managed_account_retrieve_response['updated_at'],
    }

    assert managed_account_retrieve_response == expect_results


def test_list_managed_account_transactions():
    global managed_account_transactions_list_response

    if not managed_account_list_response._data:
        return

    managed_account_id = managed_account_list_response[0]['id']
    managed_account_transactions_list_response = method.managed_accounts(managed_account_id).transactions.list()

    assert managed_account_transactions_list_response is not None
    assert isinstance(managed_account_transactions_list_response._data, list)
