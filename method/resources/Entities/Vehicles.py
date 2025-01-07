from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError

EntityVehiclesResponseStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]

class EntityVehiclesType(TypedDict):
    vin: Optional[str]
    year: Optional[str]
    make: Optional[str]
    model: Optional[str]
    series: Optional[str]
    major_color: Optional[str]
    style: Optional[str]


class EntityVehicles(TypedDict):
    id: str
    entity_id: str
    status: EntityVehiclesResponseStatusLiterals
    vehicles: Optional[List[EntityVehiclesType]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityVehiclesResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityVehiclesResource, self).__init__(config.add_path('vehicles'))

    def retrieve(self, attr_id: str) -> MethodResponse[EntityVehicles]:
        return super(EntityVehiclesResource, self)._get_with_id(attr_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[EntityVehicles]]:
        return super(EntityVehiclesResource, self)._list(params)

    def create(self) -> MethodResponse[EntityVehicles]:
        return super(EntityVehiclesResource, self)._create({})