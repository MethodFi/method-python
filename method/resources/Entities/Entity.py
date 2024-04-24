from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resource import Resource, RequestOpts, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Entities import EntityConnectResource, EntityCreditScoresResource, EntityIdentityResource, \
    EntityProductResource, EntitySensitiveResource, EntitySubscriptionsResource, EntityVerificationSessionResource


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


CreditScoreStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


EntityIndividualPhoneVerificationTypesLiterals = Literal[
    'method_sms',
    'method_verified',
    'sms',
    'tos'
]


CreditScoreStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


CreditReportBureausLiterals = Literal[
    'experian',
    'equifax',
    'transunion'
]

EntitySensitiveFieldsLiterals = Literal[
    'first_name',
    'last_name',
    'phone',
    'phone_history',
    'email',
    'dob',
    'address',
    'address_history',
    'ssn_4',
    'ssn_6',
    'ssn_9',
    'identities'
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


class EntityListOpts(ResourceListOpts):
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
    authenticated: bool
    cxn_id: List[str]
    accounts: List[str]


class EntityCreditScoresFactorsType(TypedDict):
    code: str
    description: str


class AnswerOpts(TypedDict):
    question_id: str
    answer_id: str


class EntityUpdateAuthOpts(TypedDict):
    answers: List[AnswerOpts]


class EntityUpdateAuthResponse(TypedDict):
    questions: List[EntityQuestion]
    authenticated: bool
    cxn_id: Optional[str]
    accounts: List[str]


class EntityManualAuthOpts(TypedDict):
    format: str
    bureau: CreditReportBureausLiterals
    raw_report: Dict[str, Any]


class EntityManualAuthResponse(TypedDict):
    authenticated: bool
    accounts: List[str]


class EntityGetCreditScoreResponse(TypedDict):
    score: int
    updated_at: str


class AnswerOpts(TypedDict):
    question_id: str
    answer_id: str


class EntityUpdateAuthOpts(TypedDict):
    answers: List[AnswerOpts]


class EntityUpdateAuthResponse(TypedDict):
    questions: List[EntityQuestion]
    cxn_id: Optional[str]


class EntitySubResources:
    connect: EntityConnectResource
    credit_scores: EntityCreditScoresResource
    identities: EntityIdentityResource
    products: EntityProductResource
    sensitive: EntitySensitiveResource
    subscriptions: EntitySubscriptionsResource
    verification_sessions: EntityVerificationSessionResource

    def __init__(self, _id: str, config: Configuration):
        self.connect = EntityConnectResource(config.add_path(_id))
        self.credit_scores = EntityCreditScoresResource(config.add_path(_id))
        self.identities = EntityIdentityResource(config.add_path(_id))
        self.products = EntityProductResource(config.add_path(_id))
        self.sensitive = EntitySensitiveResource(config.add_path(_id))
        self.subscriptions = EntitySubscriptionsResource(config.add_path(_id))
        self.verification_sessions = EntityVerificationSessionResource(config.add_path(_id))


class EntityResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityResource, self).__init__(config.add_path('entities'))

    def __call__(self, _id: str) -> EntitySubResources:
        return EntitySubResources(_id, self.config)

    def create(self, opts: EntityCreateOpts, request_opts: Optional[RequestOpts] = None) -> Entity:
        return super(EntityResource, self)._create(opts, request_opts)

    def update(self, _id: str, opts: EntityCreateOpts) -> Entity:
        return super(EntityResource, self)._update_with_id(_id, opts)

    def retrieve(self, _id: str) -> Entity:
        return super(EntityResource, self)._get_with_id(_id)

    def list(self, params: EntityListOpts = None) -> List[Entity]:
        return super(EntityResource, self)._list(params)

    def refresh_capabilities(self, _id: str) -> Entity:
        return super(EntityResource, self)._create_with_sub_path('{_id}/refresh_capabilities'.format(_id=_id), {})

    def withdraw_consent(self, _id: str) -> Entity:
        return super(EntityResource, self)._create_with_sub_path(
            '{_id}/consent'.format(_id=_id),
            {'type': 'withdraw', 'reason': 'entity_withdrew_consent'}
        )