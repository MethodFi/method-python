from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from typing import Optional, Literal, List, TypedDict


AttributesBehaviorsLiterals = Literal[
    'new_soft_inquiry'
]


class SimulateEntityAttributesOpts(TypedDict):
    behaviors: List[AttributesBehaviorsLiterals]


class SimulateAttributesInstance(Resource):
    def __init__(self, entity_id: str, config: Configuration):
        super(SimulateAttributesInstance, self).__init__(config.add_path(entity_id))

    def create(self, opts: SimulateEntityAttributesOpts) -> MethodResponse[Optional[None]]:
        return super(SimulateAttributesInstance, self)._create(opts)


class SimulateAttributesResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateAttributesResource, self).__init__(config.add_path('attributes'))

    def __call__(self, entity_id: str) -> SimulateAttributesInstance:
        return SimulateAttributesInstance(entity_id, self.config)
