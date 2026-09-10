from typing import TypedDict, Optional

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Payments.Payment import Payment, PaymentStatusesLiterals
from method.resources.Simulate.PaymentInstruments import SimulatePaymentInstrumentsResource


class SimulatePaymentUpdateOpts(TypedDict):
    status: PaymentStatusesLiterals
    error_code: Optional[int]


class SimulatePaymentResource(Resource):
    payment_instruments: SimulatePaymentInstrumentsResource

    def __init__(self, config: Configuration):
        _config = config.add_path('payments')
        super(SimulatePaymentResource, self).__init__(_config)
        self.payment_instruments = SimulatePaymentInstrumentsResource(_config)

    def update(self, _id: str, opts: SimulatePaymentUpdateOpts) -> MethodResponse[Payment]:
        return super(SimulatePaymentResource, self)._post_with_id(_id, opts)
