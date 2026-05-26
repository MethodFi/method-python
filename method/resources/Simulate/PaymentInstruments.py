from typing import TypedDict, Optional

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Payments.Payment import Payment


class SimulatePaymentViaInstrumentOpts(TypedDict):
    amount: int


class SimulatePaymentInstrumentInstance(Resource):
    def __init__(self, pmt_inst_id: str, config: Configuration):
        super(SimulatePaymentInstrumentInstance, self).__init__(config.add_path(pmt_inst_id))

    def create(self, opts: SimulatePaymentViaInstrumentOpts) -> MethodResponse[Payment]:
        return super(SimulatePaymentInstrumentInstance, self)._create(opts)


class SimulatePaymentInstrumentResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulatePaymentInstrumentResource, self).__init__(config.add_path('payment_instruments'))

    def __call__(self, pmt_inst_id: str) -> SimulatePaymentInstrumentInstance:
        return SimulatePaymentInstrumentInstance(pmt_inst_id, self.config)
