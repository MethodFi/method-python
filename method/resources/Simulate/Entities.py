from method.resource import Resource
from method.configuration import Configuration
from method.resources.Simulate.CreditScores import SimulateCreditScoresResource


class SimulateEntitySubResources:
    credit_scores: SimulateCreditScoresResource

    def __init__(self, _id: str, config: Configuration):
        self.credit_scores = SimulateCreditScoresResource(config.add_path(_id))

  
class SimulateEntityResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateEntityResource, self).__init__(config.add_path('entities'))

    def __call__(self, ent_id) -> SimulateEntitySubResources:
        return SimulateEntitySubResources(ent_id, self.config)
