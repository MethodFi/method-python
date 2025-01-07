from typing import TypedDict, Optional, List, Dict, Any

from method.resource import MethodResponse, Resource, RequestOpts, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Entities.Attributes import EntityAttributesResource
from method.resources.Entities.Types import EntityTypesLiterals, EntityCapabilitiesLiterals, EntityStatusesLiterals, \
    CreditReportBureausLiterals, EntityIndividual, EntityCorporation, EntityAddress
from method.resources.Entities.Connect import EntityConnectResource
from method.resources.Entities.CreditScores import EntityCreditScoresResource
from method.resources.Entities.Identities import EntityIdentityResource
from method.resources.Entities.Vehicles import EntityVehiclesResource
from method.resources.Entities.Products import EntityProductResource
from method.resources.Entities.Sensitive import EntitySensitiveResource
from method.resources.Entities.Subscriptions import EntitySubscriptionsResource
from method.resources.Entities.VerificationSessions import EntityVerificationSessionResource


class EntityCreateOpts(TypedDict):
    type: EntityTypesLiterals
    individual: Optional[EntityIndividual]
    corporation: Optional[EntityCorporation]
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


class Entity(TypedDict):
    id: str
    type: EntityTypesLiterals
    individual: Optional[EntityIndividual]
    corporation: Optional[EntityCorporation]
    capabilities: List[EntityCapabilitiesLiterals]
    available_capabilities: List[EntityCapabilitiesLiterals]
    pending_capabilities: List[EntityCapabilitiesLiterals]
    address: EntityAddress
    status: EntityStatusesLiterals
    error: Optional[ResourceError]
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str


class EntitySubResources:
    attributes: EntityAttributesResource
    connect: EntityConnectResource
    credit_scores: EntityCreditScoresResource
    identities: EntityIdentityResource
    vehicles: EntityVehiclesResource
    products: EntityProductResource
    sensitive: EntitySensitiveResource
    subscriptions: EntitySubscriptionsResource
    verification_sessions: EntityVerificationSessionResource

    def __init__(self, _id: str, config: Configuration):
        self.attributes = EntityAttributesResource(config.add_path(_id))
        self.connect = EntityConnectResource(config.add_path(_id))
        self.credit_scores = EntityCreditScoresResource(config.add_path(_id))
        self.identities = EntityIdentityResource(config.add_path(_id))
        self.vehicles = EntityVehiclesResource(config.add_path(_id))
        self.products = EntityProductResource(config.add_path(_id))
        self.sensitive = EntitySensitiveResource(config.add_path(_id))
        self.subscriptions = EntitySubscriptionsResource(config.add_path(_id))
        self.verification_sessions = EntityVerificationSessionResource(config.add_path(_id))


class EntityResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityResource, self).__init__(config.add_path('entities'))

    def __call__(self, _id: str) -> EntitySubResources:
        return EntitySubResources(_id, self.config)

    def create(self, opts: EntityCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[Entity]:
        return super(EntityResource, self)._create(opts, request_opts)

    def update(self, _id: str, opts: EntityCreateOpts) -> MethodResponse[Entity]:
        return super(EntityResource, self)._update_with_id(_id, opts)

    def retrieve(self, _id: str) -> MethodResponse[Entity]:
        return super(EntityResource, self)._get_with_id(_id)

    def list(self, params: EntityListOpts = None) -> MethodResponse[List[Entity]]:
        return super(EntityResource, self)._list(params)

    def withdraw_consent(self, _id: str) -> MethodResponse[Entity]:
        return super(EntityResource, self)._create_with_sub_path(
            '{_id}/consent'.format(_id=_id),
            {'type': 'withdraw', 'reason': 'entity_withdrew_consent'}
        )
