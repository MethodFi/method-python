from typing import TypedDict, Optional, List, Dict, Any, Literal, Union

from method.resource import MethodResponse, Resource, RequestOpts, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Entities.Attributes import EntityAttributes, EntityAttributesResource
from method.resources.Entities.Types import EntityTypesLiterals, EntityCapabilitiesLiterals, EntityStatusesLiterals, \
    CreditReportBureausLiterals, EntityExpandableFieldsLiterals, EntityIndividual, EntityCorporation, EntityAddress, \
    EntityProductTypesLiterals, EntityVerification
from method.resources.Entities.Connect import EntityConnect, EntityConnectResource
from method.resources.Entities.CreditScores import EntityCreditScores, EntityCreditScoresResource
from method.resources.Entities.Identities import EntityIdentityResource
from method.resources.Entities.ManualConnect import EntityManualConnectResource
from method.resources.Entities.Vehicles import EntityVehicles, EntityVehiclesResource
from method.resources.Entities.Products import EntityProductResource
from method.resources.Entities.Sensitive import EntitySensitiveResource
from method.resources.Entities.Subscriptions import EntitySubscriptionNamesLiterals, EntitySubscriptionsResource
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
    expand: Optional[List[EntityExpandableFieldsLiterals]]


class EntityWithdrawConsentOpts(TypedDict):
    type: Literal['withdraw']
    reason: Optional[Literal['entity_withdrew_consent']]


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
    products: Optional[List[EntityProductTypesLiterals]]
    restricted_products: Optional[List[EntityProductTypesLiterals]]
    subscriptions: Optional[List[EntitySubscriptionNamesLiterals]]
    available_subscriptions: Optional[List[EntitySubscriptionNamesLiterals]]
    restricted_subscriptions: Optional[List[EntitySubscriptionNamesLiterals]]
    verification: Optional[EntityVerification]
    connect: Optional[Union[str, EntityConnect]]
    credit_score: Optional[Union[str, EntityCreditScores]]
    attribute: Optional[Union[str, EntityAttributes]]
    vehicle: Optional[Union[str, EntityVehicles]]
    created_at: str
    updated_at: str


class EntitySubResources:
    attributes: EntityAttributesResource
    connect: EntityConnectResource
    credit_scores: EntityCreditScoresResource
    identities: EntityIdentityResource
    manual_connect: EntityManualConnectResource
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
        self.manual_connect = EntityManualConnectResource(config.add_path(_id))
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

    def retrieve(self, _id: str, params: Optional[Dict[str, List[EntityExpandableFieldsLiterals]]] = None) -> MethodResponse[Entity]:
        return super(EntityResource, self)._get_with_sub_path_and_params(_id, params)

    def list(self, params: EntityListOpts = None) -> MethodResponse[List[Entity]]:
        return super(EntityResource, self)._list(params)

    def withdraw_consent(self, _id: str, data: EntityWithdrawConsentOpts = { 'type': 'withdraw', 'reason': 'entity_withdrew_consent' }, request_opts: Optional[RequestOpts] = None) -> MethodResponse[Entity]: # pylint: disable=dangerous-default-value
        return super(EntityResource, self)._create_with_sub_path('{_id}/consent'.format(_id=_id), data, request_opts=request_opts)
