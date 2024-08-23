from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


AccountCurrencyTypesLiterals = Literal[
    'USD'
]


AccountTransactionStatusLiterals = Literal[
    'cleared',
    'auth',
    'refund',
    'unknown'
]


class AccountTransactionMerchant(TypedDict):
    name: str
    category_code: str
    city: str
    state: str
    country: str
    acquirer_bin: str
    acquirer_card_acceptor_id: str


class AccountTransactionNetworkData(TypedDict):
    visa_merchant_id: Optional[str]
    visa_merchant_name: Optional[str]
    visa_store_id: Optional[str]
    visa_store_name: Optional[str]


class AccountTransaction(TypedDict):
    id: str
    account_id: str
    merchant: AccountTransactionMerchant
    network: str
    network_data: AccountTransactionNetworkData
    amount: int
    currency: AccountCurrencyTypesLiterals
    billing_amount: int
    billing_currency: AccountCurrencyTypesLiterals
    status: AccountTransactionStatusLiterals
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountTransactionsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountTransactionsResource, self).__init__(config.add_path('transactions'))

    def retrieve(self, txn_id: str) -> MethodResponse[AccountTransaction]:
        return super(AccountTransactionsResource, self)._get_with_id(txn_id)

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountTransaction]]:
        return super(AccountTransactionsResource, self)._list(params)
