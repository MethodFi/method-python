from method.resource import Resource
from method.configuration import Configuration
from method.resources.Simulate.Payments import SimulatePaymentResource
from method.resources.Simulate.Transactions import SimulateTransactionsResource


class SimulateResource(Resource):
    payments: SimulatePaymentResource
    transactions: SimulateTransactionsResource

    def __init__(self, config: Configuration):
        _config = config.add_path('simulate')
        super(SimulateResource, self).__init__(_config)
        self.payments = SimulatePaymentResource(_config)
        self.transactions = SimulateTransactionsResource(_config)
