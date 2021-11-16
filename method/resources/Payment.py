from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resource import Resource, RequestOpts
from method.configuration import Configuration


PaymentStatusesLiterals = Literal[
    'pending',
    'canceled',
    'processing',
    'failed',
    'sent',
    'reversed'
]


PaymentFundStatusesLiterals = Literal[
    'hold',
    'pending',
    'requested',
    'received',
    'sent',
    'unknown'
]


class Payment(TypedDict):
    id: str
    source: str
    destination: str
    amount: int
    description: str
    status: PaymentStatusesLiterals
    fund_status: PaymentFundStatusesLiterals
    error: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str


class PaymentCreateOpts(TypedDict):
    amount: int
    source: str
    destination: str
    description: str
    metadata: Optional[Dict[str, Any]]


class PaymentResource(Resource):
    def __init__(self, config: Configuration):
        super(PaymentResource, self).__init__(config.add_path('payments'))

    def get(self, _id: str) -> Payment:
        return super(PaymentResource, self)._get_with_id(_id)

    def list(self) -> List[Payment]:
        return super(PaymentResource, self)._list(None)

    def create(self, opts: PaymentCreateOpts, request_opts: Optional[RequestOpts] = None) -> Payment:
        return super(PaymentResource, self)._create(opts, request_opts)

    def delete(self, _id: str) -> Payment:
        return super(PaymentResource, self)._delete(_id)
