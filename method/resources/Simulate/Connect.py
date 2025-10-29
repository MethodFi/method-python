from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from typing import Optional, Literal, List, TypedDict


ConnectBehaviorsLiterals = Literal[
    'new_credit_card_account',
    'new_auto_loan_account',
    'new_mortgage_account',
    'new_student_loan_account',
    'new_personal_loan_account'
]


class SimulateEntityConnectOpts(TypedDict):
    behaviors: List[ConnectBehaviorsLiterals]


class SimulateConnectInstance(Resource):
    def __init__(self, entity_id: str, config: Configuration):
        super(SimulateConnectInstance, self).__init__(config.add_path(entity_id))

    def create(self, opts: SimulateEntityConnectOpts) -> MethodResponse[Optional[None]]:
        """
        For Entities that have been successfully verified, you may simulate Connect in the dev environment.
        https://docs.methodfi.com/reference/simulations/connect/create
        
        Args:
            opts: SimulateEntityConnectOpts
        """
        return super(SimulateConnectInstance, self)._create(opts)


class SimulateConnectResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateConnectResource, self).__init__(config.add_path('connect'))

    def __call__(self, entity_id: str) -> SimulateConnectInstance:
        return SimulateConnectInstance(entity_id, self.config)
