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
    name: str
    status: EntityProductTypeStatusLiterals
    status_error: Optional[ResourceError]
    latest_request_id: str
    latest_successful_request_id: Optional[str]
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

    def list(self) -> MethodResponse[EntityProductListResponse]:
        return super(EntityProductResource, self)._list()
