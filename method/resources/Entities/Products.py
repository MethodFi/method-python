from typing import TypedDict, Optional, Literal

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.errors import ResourceError


EntityProductTypeStatusLiterals = Literal[
    'unavailable',
    'available',
    'restricted'
]


class EntityProduct(TypedDict):
    id: str
    name: str
    status: EntityProductTypeStatusLiterals
    status_error: Optional[ResourceError]
    latest_request_id: str
    is_subscribable: bool
    created_at: str
    updated_at: str


class EntityProductListResponse(TypedDict):
    attribute: Optional[EntityProduct]
    connect: Optional[EntityProduct]
    credit_score: Optional[EntityProduct]
    identity: Optional[EntityProduct]
    vehicles: Optional[EntityProduct]


class EntityProductResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityProductResource, self).__init__(config.add_path('products'))

    def retrieve(self, prd_id: str) -> MethodResponse[EntityProduct]:
        return super(EntityProductResource, self)._get_with_id(prd_id)

    def list(self) -> MethodResponse[EntityProductListResponse]:
        return super(EntityProductResource, self)._list()
