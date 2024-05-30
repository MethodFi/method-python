from method.resource import Resource
from method.configuration import Configuration
from method.resources.Simulate.Payments import SimulatePaymentResource
from method.resources.Simulate.Accounts import SimulateAccountResource


class SimulateResource(Resource):
    payments: SimulatePaymentResource
    accounts: SimulateAccountResource

    def __init__(self, config: Configuration):
        _config = config.add_path('simulate')
        super(SimulateResource, self).__init__(_config)
        self.payments = SimulatePaymentResource(_config)
        self.accounts = SimulateAccountResource(_config)
