from method.resource import Resource
from method.configuration import Configuration
from method.resources.Simulate.Transactions import SimulateTransactionsResource


class SimulateAccountSubResources:
    transactions: SimulateTransactionsResource

    def __init__(self, _id: str, config: Configuration):
        self.transactions = SimulateTransactionsResource(config.add_path(_id))

  
class SimulateAccountResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateAccountResource, self).__init__(config.add_path('accounts'))

    def __call__(self, acc_id) -> SimulateAccountSubResources:
        return SimulateAccountSubResources(acc_id, self.config)
