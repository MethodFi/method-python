from method.resource import Resource
from method.configuration import Configuration
from method.resources.SimulatePayment import SimulatePaymentResource


class SimulateResource(Resource):
    payments: SimulatePaymentResource

    def __init__(self, config: Configuration):
        _config = config.add_path('simulate')
        super(SimulateResource, self).__init__(_config)
        self.payments = SimulatePaymentResource(_config)
