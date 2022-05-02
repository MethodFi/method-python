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
    'payments:limited-send',
    'data:retrieve'
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
    available_capabilities: List[EntityCapabilitiesLiterals]
    pending_capabilities: List[EntityCapabilitiesLiterals]
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


class EntityListOpts(TypedDict):
    to_date: Optional[str]
    from_date: Optional[str]
    page: Optional[int]
    page_limit: Optional[int]
    page_cursor: Optional[str]
    status: Optional[str]
    type: Optional[str]

class EntityAnswer(TypedDict):
    id: str
    text: str

class EntityQuestion(TypedDict):
    id: str
    text: Optional[str]
    answers: List[EntityAnswer]

class EntityQuestionResponse(TypedDict):
    questions: List[EntityQuestion]

class AnswerOpts(TypedDict):
    question_id: str
    answer_id: str

class EntityUpdateAuthOpts(TypedDict):
  answers: List[AnswerOpts]

class EntityUpdateAuthResponse(TypedDict):
  questions: List[EntityQuestion]
  cxn_id: Optional[str]


class EntityResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityResource, self).__init__(config.add_path('entities'))

    def create(self, opts: EntityCreateOpts, request_opts: Optional[RequestOpts] = None) -> Entity:
        return super(EntityResource, self)._create(opts, request_opts)

    def update(self, _id: str, opts: EntityCreateOpts) -> Entity:
        return super(EntityResource, self)._update_with_id(_id, opts)

    def get(self, _id: str) -> Entity:
        return super(EntityResource, self)._get_with_id(_id)

    def list(self, params: EntityListOpts = None) -> List[Entity]:
        return super(EntityResource, self)._list(params)
    
    def create_auth_session(self, _id: str) -> EntityQuestionResponse:
        return super(EntityResource, self)._create_with_sub_path('{_id}/auth_session'.format(_id=_id), {})

    def update_auth_session(self, _id: str, opts: EntityUpdateAuthOpts) -> EntityUpdateAuthResponse:
        return super(EntityResource, self)._update_with_sub_path('{_id}/auth_session'.format(_id=_id), opts)

    def refresh_capabilities(self, _id: str) -> Entity:
        return super(EntityResource, self)._create_with_sub_path('{_id}/refresh_capabilities'.format(_id=_id), {})
