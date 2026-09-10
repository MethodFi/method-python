from typing import TypedDict, Optional

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Payments.Payment import Payment


class SimulatePaymentInstrumentCreateOpts(TypedDict):
    amount: int
    ach_reference_id: Optional[str]
    description: Optional[str]


class SimulatePaymentInstrumentInstanceResource(Resource):
    def __init__(self, pmt_inst_id: str, config: Configuration):
        super(SimulatePaymentInstrumentInstanceResource, self).__init__(config.add_path(pmt_inst_id))

    def create(self, opts: SimulatePaymentInstrumentCreateOpts) -> MethodResponse[Payment]:
        return super(SimulatePaymentInstrumentInstanceResource, self)._create(opts)


class SimulatePaymentInstrumentsResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulatePaymentInstrumentsResource, self).__init__(config.add_path('payment_instruments'))

    def __call__(self, pmt_inst_id: str) -> SimulatePaymentInstrumentInstanceResource:
        return SimulatePaymentInstrumentInstanceResource(pmt_inst_id, self.config)
