import os
import pytest
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

# Managed accounts cannot be created via the public API; they are provisioned per-team by
# Method. If the dev team has none, set MANAGED_ACCOUNT_ID to a macc_... id provisioned for
# the team to exercise the retrieve and transactions tests.
MANAGED_ACCOUNT_ID = os.getenv('MANAGED_ACCOUNT_ID')

method = Method(env='dev', api_key=API_KEY)

MANAGED_ACCOUNT_EXPECTED_KEYS = ['id', 'routing', 'number', 'current_balance', 'available_balance']
MANAGED_ACCOUNT_TRANSACTION_EXPECTED_KEYS = ['id', 'description', 'date', 'amount']


def get_test_managed_account_id():
    if MANAGED_ACCOUNT_ID:
        return MANAGED_ACCOUNT_ID

    managed_accounts_list_response = method.managed_accounts.list()

    if len(managed_accounts_list_response) == 0:
        pytest.skip('No managed accounts provisioned for the dev team and MANAGED_ACCOUNT_ID is not set.')

    return managed_accounts_list_response[0]['id']


def test_list_managed_accounts():
    managed_accounts_list_response = method.managed_accounts.list()

    assert isinstance(managed_accounts_list_response.to_dict(), list)

    for managed_account in managed_accounts_list_response:
        for key in MANAGED_ACCOUNT_EXPECTED_KEYS:
            assert key in managed_account


def test_retrieve_managed_account():
    macc_id = get_test_managed_account_id()

    managed_accounts_retrieve_response = method.managed_accounts.retrieve(macc_id)

    assert managed_accounts_retrieve_response['id'] == macc_id

    for key in MANAGED_ACCOUNT_EXPECTED_KEYS:
        assert key in managed_accounts_retrieve_response


def test_list_managed_account_transactions():
    macc_id = get_test_managed_account_id()

    managed_account_transactions_list_response = method.managed_accounts(macc_id).transactions.list()

    assert isinstance(managed_account_transactions_list_response.to_dict(), list)

    for transaction in managed_account_transactions_list_response:
        for key in MANAGED_ACCOUNT_TRANSACTION_EXPECTED_KEYS:
            assert key in transaction
