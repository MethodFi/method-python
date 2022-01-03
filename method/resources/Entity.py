from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resource import Resource, RequestOpts
from method.configuration import Configuration
from method.errors import ResourceError


EntityTypesLiterals = Literal[
    'individual',
    'c_corporation',
    's_corporation',
    'llc',
    'partnership',
    'sole_proprietorship',
    'receive_only'
]


EntityCapabilitiesLiterals = Literal[
    'payments:send',
    'payments:receive',
    'payments:limited-send'
]


EntityStatusesLiterals = Literal[
    'active',
    'incomplete',
    'disabled'
]


class EntityIndividual(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    dob: Optional[str]


class EntityAddress(TypedDict):
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]


class EntityCorporationOwner(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    dob: Optional[str]
    address: EntityAddress


class EntityCorporation(TypedDict):
    name: Optional[str]
    dba: Optional[str]
    ein: Optional[str]
    owners: List[EntityCorporationOwner]


class EntityReceiveOnly(TypedDict):
    name: str
    phone: Optional[str]
    email: Optional[str]


class Entity(TypedDict):
    id: str
    type: EntityTypesLiterals
    individual: Optional[EntityIndividual]
    corporation: Optional[EntityCorporation]
    receive_only: Optional[EntityReceiveOnly]
    capabilities: List[EntityCapabilitiesLiterals]
    address: EntityAddress
    status: EntityStatusesLiterals
    error: Optional[ResourceError]
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str


class EntityCreateOpts(TypedDict):
    type: EntityTypesLiterals
    individual: Optional[EntityIndividual]
    corporation: Optional[EntityCorporation]
    receive_only: Optional[EntityReceiveOnly]
    address: Optional[EntityAddress]
    metadata: Optional[Dict[str, Any]]


class EntityUpdateOpts(TypedDict):
    individual: Optional[EntityIndividual]
    corporation: Optional[EntityCorporation]
    address: Optional[EntityAddress]


class EntityResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityResource, self).__init__(config.add_path('entities'))

    def create(self, opts: EntityCreateOpts, request_opts: Optional[RequestOpts] = None) -> Entity:
        return super(EntityResource, self)._create(opts, request_opts)

    def update(self, _id: str, opts: EntityCreateOpts) -> Entity:
        return super(EntityResource, self)._update_with_id(_id, opts)

    def get(self, _id: str) -> Entity:
        return super(EntityResource, self)._get_with_id(_id)

    def list(self) -> List[Entity]:
        return super(EntityResource, self)._list(None)
