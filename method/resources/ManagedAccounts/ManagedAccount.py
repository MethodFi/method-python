from typing import TypedDict, Optional, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration


class ManagedAccountTransaction(TypedDict):
    id: str
    managed_account_id: str
    amount: int
    type: str
    status: str
    description: Optional[str]
    created_at: str
    updated_at: str


class ManagedAccount(TypedDict):
    id: str
    type: str
    status: str
    routing_number: Optional[str]
    account_number: Optional[str]
    balance: Optional[int]
    created_at: str
    updated_at: str


class ManagedAccountTransactionsResource(Resource):
    def __init__(self, config: Configuration):
        super(ManagedAccountTransactionsResource, self).__init__(config.add_path('transactions'))

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[ManagedAccountTransaction]]:
        return super(ManagedAccountTransactionsResource, self)._list(params)


class ManagedAccountSubResources:
    transactions: ManagedAccountTransactionsResource

    def __init__(self, _id: str, config: Configuration):
        self.transactions = ManagedAccountTransactionsResource(config.add_path(_id))


class ManagedAccountResource(Resource):
    def __init__(self, config: Configuration):
        super(ManagedAccountResource, self).__init__(config.add_path('managed_accounts'))

    def __call__(self, _id: str) -> ManagedAccountSubResources:
        return ManagedAccountSubResources(_id, self.config)

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[ManagedAccount]]:
        return super(ManagedAccountResource, self)._list(params)

    def retrieve(self, _id: str) -> MethodResponse[ManagedAccount]:
        return super(ManagedAccountResource, self)._get_with_id(_id)
