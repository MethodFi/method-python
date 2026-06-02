from typing import TypedDict, List

from method.resource import MethodResponse, Resource
from method.configuration import Configuration


class VerificationSessionAmounts(TypedDict):
    amounts: List[int]


class SimulateVerificationAmountsInstance(Resource):
    def __init__(self, avf_id: str, config: Configuration):
        super(SimulateVerificationAmountsInstance, self).__init__(config.add_path(avf_id))

    def amounts(self) -> MethodResponse[VerificationSessionAmounts]:
        return super(SimulateVerificationAmountsInstance, self)._get_with_sub_path('amounts')


class SimulateVerificationSessionsResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateVerificationSessionsResource, self).__init__(config.add_path('verification_sessions'))

    def __call__(self, avf_id: str) -> SimulateVerificationAmountsInstance:
        return SimulateVerificationAmountsInstance(avf_id, self.config)
