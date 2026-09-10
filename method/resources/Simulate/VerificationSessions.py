from typing import TypedDict, List

from method.resource import MethodResponse, Resource
from method.configuration import Configuration


class SimulateVerificationSessionAmounts(TypedDict):
    amounts: List[int]


class SimulateVerificationSessionInstanceResource(Resource):
    def __init__(self, avf_id: str, config: Configuration):
        super(SimulateVerificationSessionInstanceResource, self).__init__(config.add_path(avf_id))

    def amounts(self) -> MethodResponse[SimulateVerificationSessionAmounts]:
        return super(SimulateVerificationSessionInstanceResource, self)._get_with_sub_path('amounts')


class SimulateVerificationSessionsResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateVerificationSessionsResource, self).__init__(config.add_path('verification_sessions'))

    def __call__(self, avf_id: str) -> SimulateVerificationSessionInstanceResource:
        return SimulateVerificationSessionInstanceResource(avf_id, self.config)
