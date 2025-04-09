from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from typing import List, Dict, Any
from method.resources.Entities.CreditScores import EntityCreditScoresType, EntityCreditScores


class SimulateCreditScoresInstance(Resource):
    def __init__(self, crs_id: str, config: Configuration):
        super(SimulateCreditScoresInstance, self).__init__(config.add_path(crs_id))

    def create(self, scores: List[EntityCreditScoresType]) -> MethodResponse[EntityCreditScores]:
        return super(SimulateCreditScoresInstance, self)._create({"scores": scores})


class SimulateCreditScoresResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateCreditScoresResource, self).__init__(config.add_path('credit_scores'))

    def __call__(self, crs_id: str) -> SimulateCreditScoresInstance:
        return SimulateCreditScoresInstance(crs_id, self.config)
