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
    authenticated: bool
    cxn_id: List[str]
    accounts: List[str]


class EntityCreditScoresFactorsType(TypedDict):
    code: str
    description: str


class EntityCreditScoresType(TypedDict):
    score: int
    source: CreditReportBureausLiterals
    model: str
    factors: List[EntityCreditScoresFactorsType]
    created_at: str
    factors: EntityCreditScoresFactorsType
    created_at: str


class EntityCreditScoresResponse(TypedDict):
    id: str
    status: EntityStatusesLiterals
    credit_scores: Optional[List[EntityCreditScoresType]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityCreditScoresFactorsType(TypedDict):
    code: str
    description: str


class EntityCreditScoresType(TypedDict):
    score: int
    source: CreditReportBureausLiterals
    model: str
    factors: List[EntityCreditScoresFactorsType]
    created_at: str


class EntityCreditScoresResponse(TypedDict):
    id: str
    status: EntityStatusesLiterals
    credit_scores: Optional[List[EntityCreditScoresType]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


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


class EntityKYCAddressRecordData(TypedDict):
    address: str
    city: str
    postal_code: str
    state: str
    address_term: int


class EntityIdentity(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    dob: Optional[str]
    address: Optional[EntityKYCAddressRecordData]
    ssn: Optional[str]


class EntitySensitiveResponse(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    phone_history: Optional[List[str]]
    email: Optional[str]
    dob: Optional[str]
    address: Optional[EntityKYCAddressRecordData]
    address_history: List[EntityKYCAddressRecordData]
    ssn_4: Optional[str]
    ssn_6: Optional[str]
    ssn_9: Optional[str]
    identities: List[EntityIdentity]


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

    def get_credit_score(self, _id: str) -> EntityQuestionResponse:
        return super(EntityResource, self)._get_with_sub_path('{_id}/credit_score'.format(_id=_id))

    def get_credit_scores(self, _id: str, crs_id: str) -> EntityCreditScoresResponse:
        return super(EntityResource, self)._get_with_sub_path('{_id}/credit_scores/{crs_id}'.format(_id=_id, crs_id=crs_id))

    def create_credit_scores(self, _id: str) -> EntityCreditScoresResponse:
        return super(EntityResource, self)._create_with_sub_path('{_id}/credit_scores'.format(_id=_id), {})

    def update_auth_session(self, _id: str, opts: EntityUpdateAuthOpts) -> EntityUpdateAuthResponse:
        return super(EntityResource, self)._update_with_sub_path('{_id}/auth_session'.format(_id=_id), opts)

    def create_manual_auth_session(self, _id: str, opts: EntityManualAuthOpts) -> EntityManualAuthResponse:
        return super(EntityResource, self)._create_with_sub_path('{_id}/manual_auth_session'.format(_id=_id), opts)

    def update_manual_auth_session(self, _id: str, opts: EntityManualAuthOpts) -> EntityManualAuthResponse:
        return super(EntityResource, self)._update_with_sub_path('{_id}/manual_auth_session'.format(_id=_id), opts)

    def refresh_capabilities(self, _id: str) -> Entity:
        return super(EntityResource, self)._create_with_sub_path('{_id}/refresh_capabilities'.format(_id=_id), {})

    def get_credit_score(self, _id: str) -> EntityQuestionResponse:
        return super(EntityResource, self)._get_with_sub_path('{_id}/credit_score'.format(_id=_id))

    def get_sensitive_fields(self, _id: str, fields: List[EntitySensitiveFieldsLiterals]) -> EntitySensitiveResponse:
        return super(EntityResource, self)._get_with_sub_path_and_params(
            '{_id}/sensitive'.format(_id=_id),
            {'fields[]': fields},
        )

    def withdraw_consent(self, _id: str) -> Entity:
        return super(EntityResource, self)._create_with_sub_path(
            '{_id}/consent'.format(_id=_id),
            {'type': 'withdraw', 'reason': 'entity_withdrew_consent'}
        )
