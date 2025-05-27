from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration

AccountTransactionStatusLiterals = Literal[
    'pending',
    'posted',
    'voided',
]

class AccountTransactionMerchant(TypedDict):
    name: str
    logo: Optional[str]

class AccountTransaction(TypedDict):
    id: str
    account_id: str
    descriptor: str
    amount: int
    auth_amount: int
    currency_code: str
    transaction_amount: int
    transaction_auth_amount: int
    transaction_currency_code: str
    merchant_category_code: str
    merchant: Optional[AccountTransactionMerchant]
    status: AccountTransactionStatusLiterals
    transacted_at: str
    posted_at: Optional[str]
    voided_at: Optional[str]
    original_txn_id: Optional[str]
    created_at: str
    updated_at: str
    
    


class AccountTransactionsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountTransactionsResource, self).__init__(config.add_path('transactions'))

    def retrieve(self, txn_id: str) -> MethodResponse[AccountTransaction]:
        return super(AccountTransactionsResource, self)._get_with_id(txn_id)

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountTransaction]]:
        return super(AccountTransactionsResource, self)._list(params)
