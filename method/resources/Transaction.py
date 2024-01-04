from typing import TypedDict, List

from method.resource import Resource
from method.configuration import Configuration


class Transaction(TypedDict):
    id: str
    acc_id: str
    mcc: str
    description: str
    presentable_description: str
    amount: str
    currency: str
    billing_amount: str
    billing_currency: str
    status: str
    created_at: str
    updated_at: str


class TransactionResource(Resource):
    def __init__(self, config: Configuration):
        super(TransactionResource, self).__init__(config.add_path('transactions'))

    def list(self) -> List[Transaction]:
        return super(TransactionResource, self)._list(None)

    def get(self, _id: str) -> Transaction:
        return super(TransactionResource, self)._get_with_id(_id)
