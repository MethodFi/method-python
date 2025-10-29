from method.resource import Resource
from method.configuration import Configuration
from method.resources.Simulate.CreditScores import SimulateCreditScoresResource
from method.resources.Simulate.Connect import SimulateConnectResource
from method.resources.Simulate.Attributes import SimulateAttributesResource


class SimulateEntitySubResources:
    credit_scores: SimulateCreditScoresResource
    connect: SimulateConnectResource
    attributes: SimulateAttributesResource

    def __init__(self, _id: str, config: Configuration):
        self.credit_scores = SimulateCreditScoresResource(config.add_path(_id))
        self.connect = SimulateConnectResource(config.add_path(_id))
        self.attributes = SimulateAttributesResource(config.add_path(_id))

  
class SimulateEntityResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateEntityResource, self).__init__(config.add_path('entities'))

    def __call__(self, ent_id) -> SimulateEntitySubResources:
        return SimulateEntitySubResources(ent_id, self.config)
