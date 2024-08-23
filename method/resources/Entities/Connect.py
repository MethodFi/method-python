from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.errors import ResourceError


EntityConnectResponseStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


class EntityConnect(TypedDict):
    id: str
    status: EntityConnectResponseStatusLiterals
    accounts: Optional[List[str]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityConnectResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityConnectResource, self).__init__(config.add_path('connect'))

    def retrieve(self, cxn_id: str) -> MethodResponse[EntityConnect]:
        return super(EntityConnectResource, self)._get_with_id(cxn_id)

    def create(self) -> MethodResponse[EntityConnect]:
        return super(EntityConnectResource, self)._create({})
