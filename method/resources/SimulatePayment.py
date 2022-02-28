from typing import TypedDict, Optional

from method.resource import Resource
from method.configuration import Configuration
from method.resources.Payment import Payment, PaymentStatusesLiterals


class SimulatePaymentUpdateOpts(TypedDict):
    status: PaymentStatusesLiterals
    error_code: Optional[int]


class SimulatePaymentResource(Resource):

    def __init__(self, config: Configuration):
        super(SimulatePaymentResource, self).__init__(config.add_path('payments'))

    def update(self, _id: str, opts: SimulatePaymentUpdateOpts) -> Payment:
        return super(SimulatePaymentResource, self)._post_with_id(_id, opts)
