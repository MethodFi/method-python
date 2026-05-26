from typing import TypedDict, Optional

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Payments.Payment import Payment, PaymentStatusesLiterals
from method.resources.Simulate.PaymentInstruments import SimulatePaymentInstrumentResource


class SimulatePaymentUpdateOpts(TypedDict):
    status: PaymentStatusesLiterals
    error_code: Optional[int]


class SimulatePaymentResource(Resource):
    payment_instruments: SimulatePaymentInstrumentResource

    def __init__(self, config: Configuration):
        super(SimulatePaymentResource, self).__init__(config.add_path('payments'))
        self.payment_instruments = SimulatePaymentInstrumentResource(self.config)

    def update(self, _id: str, opts: SimulatePaymentUpdateOpts) -> MethodResponse[Payment]:
        return super(SimulatePaymentResource, self)._post_with_id(_id, opts)
