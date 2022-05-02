from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resource import Resource, RequestOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Reversal import ReversalResource


PaymentStatusesLiterals = Literal[
    'pending',
    'canceled',
    'processing',
    'failed',
    'sent',
    'reversed',
    'reversal_required',
    'reversal_processing'
]


PaymentFundStatusesLiterals = Literal[
    'hold',
    'pending',
    'requested',
    'clearing',
    'failed',
    'sent',
    'unknown'
]


PaymentTypesLiterals = Literal[
    'standard',
    'clearing'
]


PaymentFeeTypesLiterals = Literal[
    'total',
    'markup'
]


class PaymentFee(TypedDict):
    type: PaymentFeeTypesLiterals
    amount: int


class Payment(TypedDict):
    id: str
    reversal_id: Optional[str]
    source_trace_id: Optional[str]
    destination_trace_id: Optional[str]
    source: str
    destination: str
    amount: int
    description: str
    status: PaymentStatusesLiterals
    fund_status: PaymentFundStatusesLiterals
    error: Optional[ResourceError]
    metadata: Optional[Dict[str, Any]]
    estimated_completion_date: Optional[str]
    source_settlement_date: Optional[str]
    destination_settlement_date: Optional[str]
    fee: Optional[PaymentFee]
    type: PaymentTypesLiterals
    created_at: str
    updated_at: str


class PaymentCreateOpts(TypedDict):
    amount: int
    source: str
    destination: str
    description: str
    metadata: Optional[Dict[str, Any]]
    fee: Optional[PaymentFee]


class PaymentListOpts(TypedDict):
    to_date: Optional[str]
    from_date: Optional[str]
    page: Optional[int]
    page_limit: Optional[int]
    page_cursor: Optional[str]
    status: Optional[str]
    type: Optional[str]
    source: Optional[str]
    destination: Optional[str]
    reversal_id: Optional[str]


class PaymentSubResources:
    reversals: ReversalResource

    def __init__(self, _id: str, config: Configuration):
        self.reversals = ReversalResource(config.add_path(_id))


class PaymentResource(Resource):
    def __init__(self, config: Configuration):
        super(PaymentResource, self).__init__(config.add_path('payments'))

    def __call__(self, _id: str) -> PaymentSubResources:
        return PaymentSubResources(_id, self.config)

    def get(self, _id: str) -> Payment:
        return super(PaymentResource, self)._get_with_id(_id)

    def list(self, params: Optional[PaymentListOpts] = None) -> List[Payment]:
        return super(PaymentResource, self)._list(params)

    def create(self, opts: PaymentCreateOpts, request_opts: Optional[RequestOpts] = None) -> Payment:
        return super(PaymentResource, self)._create(opts, request_opts)

    def delete(self, _id: str) -> Payment:
        return super(PaymentResource, self)._delete(_id)
