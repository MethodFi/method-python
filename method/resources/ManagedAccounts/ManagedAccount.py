from typing import TypedDict, Optional, List

from method.resource import MethodResponse, Resource
from method.configuration import Configuration


class ManagedAccount(TypedDict):
    id: str
    routing: str
    number: str
    current_balance: int
    available_balance: int


class ManagedAccountTransaction(TypedDict):
    id: str
    description: str
    date: str
    amount: int


class ManagedAccountTransactionListOpts(TypedDict):
    page_limit: Optional[int]
    from_date: Optional[str]
    to_date: Optional[str]
    page_cursor: Optional[str]


class ManagedAccountTransactionsResource(Resource):
    def __init__(self, config: Configuration):
        super(ManagedAccountTransactionsResource, self).__init__(config.add_path('transactions'))

    def list(self, params: Optional[ManagedAccountTransactionListOpts] = None) -> MethodResponse[List[ManagedAccountTransaction]]:
        return super(ManagedAccountTransactionsResource, self)._list(params)


class ManagedAccountSubResources:
    transactions: ManagedAccountTransactionsResource

    def __init__(self, _id: str, config: Configuration):
        self.transactions = ManagedAccountTransactionsResource(config.add_path(_id))


class ManagedAccountResource(Resource):
    def __init__(self, config: Configuration):
        super(ManagedAccountResource, self).__init__(config.add_path('managed_accounts'))

    def __call__(self, macc_id: str) -> ManagedAccountSubResources:
        return ManagedAccountSubResources(macc_id, self.config)

    def list(self) -> MethodResponse[List[ManagedAccount]]:
        return super(ManagedAccountResource, self)._list(None)

    def retrieve(self, macc_id: str) -> MethodResponse[ManagedAccount]:
        return super(ManagedAccountResource, self)._get_with_id(macc_id)
