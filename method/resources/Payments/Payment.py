from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resource import MethodResponse, Resource, RequestOpts, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


PaymentStatusesLiterals = Literal[
    'pending',
    'canceled',
    'processing',
    'failed',
    'sent',
    'posted',
    'reversed',
    'reversal_required',
    'reversal_processing',
    'settled',
    'cashed',
    'delivered',
    'error',
    'returned'
]


PaymentDirectionStatusesLiterals = Literal[
    'pending',
    'canceled',
    'processing',
    'sent',
    'posted',
    'cashed',
    'returned'
]


PaymentFundStatusesLiterals = Literal[
    'hold',
    'pending',
    'requested',
    'clearing',
    'failed',
    'sent',
    'posted',
    'unknown',
    'transmitting',
    'transmitted',
    'cashed',
    'pending_consolidation',
    'pending_clearing'
]


PaymentTypesLiterals = Literal[
    'standard',
    'clearing'
]


PaymentFeeTypesLiterals = Literal[
    'total'
]


PaymentDestinationPaymentMethodsLiterals = Literal[
    'paper',
    'electronic'
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
    description: Optional[str]
    status: PaymentStatusesLiterals
    fund_status: Optional[PaymentFundStatusesLiterals]
    error: Optional[ResourceError]
    metadata: Optional[Dict[str, Any]]
    estimated_completion_date: Optional[str]
    source_settlement_date: Optional[str]
    destination_settlement_date: Optional[str]
    destination_posted_date: Optional[str]
    source_status: Optional[PaymentDirectionStatusesLiterals]
    destination_status: Optional[PaymentDirectionStatusesLiterals]
    destination_payment_method: Optional[PaymentDestinationPaymentMethodsLiterals]
    fee: Optional[PaymentFee]
    idempotency_key: Optional[str]
    payment_instrument: Optional[str]
    reversal_account: Optional[str]
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
    dry_run: Optional[bool]
    reversal_account: Optional[str]


class PaymentListOpts(ResourceListOpts):
    status: Optional[str]
    type: Optional[str]
    source: Optional[str]
    destination: Optional[str]
    reversal_id: Optional[str]
    source_holder_id: Optional[str]
    destination_holder_id: Optional[str]
    acc_id: Optional[str]
    holder_id: Optional[str]


from method.resources.Payments.Reversal import ReversalResource


class PaymentSubResources:
    reversals: ReversalResource

    def __init__(self, _id: str, config: Configuration):
        self.reversals = ReversalResource(config.add_path(_id))


class PaymentResource(Resource):
    def __init__(self, config: Configuration):
        super(PaymentResource, self).__init__(config.add_path('payments'))

    def __call__(self, _id: str) -> PaymentSubResources:
        return PaymentSubResources(_id, self.config)

    def retrieve(self, _id: str) -> MethodResponse[Payment]:
        return super(PaymentResource, self)._get_with_id(_id)

    def list(self, params: Optional[PaymentListOpts] = None) -> MethodResponse[List[Payment]]:
        return super(PaymentResource, self)._list(params)

    def create(self, opts: PaymentCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[Payment]:
        return super(PaymentResource, self)._create(opts, request_opts)

    def delete(self, _id: str) -> MethodResponse[Payment]:
        return super(PaymentResource, self)._delete(_id)
