from method.resource import Resource
from method.configuration import Configuration
from method.resources.Accounts.Transactions import AccountTransaction

class SimulateTransactionsResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateTransactionsResource, self).__init__(config.add_path('transactions'))

    def create(self) -> AccountTransaction:
        return super(SimulateTransactionsResource, self)._create({})
