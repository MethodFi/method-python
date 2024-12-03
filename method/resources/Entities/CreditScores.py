from typing import TypedDict, Optional, List, Literal

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Entities.Types import EntityStatusesLiterals, CreditReportBureausLiterals


CreditScoresModelLiterals = Literal[
    'vantage_4',
    'vantage_3'
]


class EntityCreditScoresFactorsType(TypedDict):
    code: str
    description: str


class EntityCreditScoresType(TypedDict):
    score: int
    source: CreditReportBureausLiterals
    model: CreditScoresModelLiterals
    factors: List[EntityCreditScoresFactorsType]
    created_at: str
    factors: EntityCreditScoresFactorsType
    created_at: str


class EntityCreditScores(TypedDict):
    id: str
    status: EntityStatusesLiterals
    credit_scores: Optional[List[EntityCreditScoresType]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityCreditScoresResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityCreditScoresResource, self).__init__(config.add_path('credit_scores'))

    def retrieve(self, crs_id: str) -> MethodResponse[EntityCreditScores]:
        return super(EntityCreditScoresResource, self)._get_with_id(crs_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[EntityCreditScores]]:
        return super(EntityCreditScoresResource, self)._list(params)

    def create(self) -> MethodResponse[EntityCreditScores]:
        return super(EntityCreditScoresResource, self)._create({})
