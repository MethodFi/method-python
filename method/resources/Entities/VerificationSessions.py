from typing import TypedDict, Optional, List, Literal

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


EntityVerificationSessionStatusLiterals = Literal[
    'verified',
    'in_progress',
    'pending',
    'failed'
]


EntityVerificationSessionMethodsLiterals = Literal[
    'sms',
    'sna',
    'byo_sms',
    'byo_kyc',
    'kba',
    'element',
    'method_verified'
]


EntityVerificationSessionTypeLiterals = Literal[
    'phone',
    'identity'
]


class EntityPhoneSmsVerification(TypedDict):
    timestamp: str


class EntityPhoneSmsVerificationUpdate(TypedDict):
    sms_code: str


class EntityPhoneSnaVerification(TypedDict):
    urls: str


class EntityByoKycVerification(TypedDict):
    authenticated: bool


class EntityKbaVerificationAnswer(TypedDict):
    id: str
    text: str


class EntityKbaVerificationAnswerUpdate(TypedDict):
    question_id: str
    answer_id: str


class EntityKbaVerificationQuestion(TypedDict):
    selected_answer: Optional[str]
    id: str
    text: str
    answers: List[EntityKbaVerificationAnswer]


class EntityKbaVerification(TypedDict):
    questions: List[EntityKbaVerificationQuestion]
    authenticated: bool


class EntityVerificationSessionCreateOpts(TypedDict):
    type: EntityVerificationSessionTypeLiterals
    method: EntityVerificationSessionMethodsLiterals
    sms: Optional[object]
    sna: Optional[object]
    byo_sms: Optional[EntityPhoneSmsVerification]
    byo_kyc: Optional[object]
    kba: Optional[object]


class EntityVerificationSessionUpdateOpts(TypedDict):
    type: EntityVerificationSessionTypeLiterals
    method: EntityVerificationSessionMethodsLiterals
    sms: Optional[EntityPhoneSmsVerificationUpdate]
    sma: Optional[object]
    kba: Optional[EntityKbaVerificationAnswerUpdate]


class EntityVerificationSession(TypedDict):
    id: str
    entity_id: str
    status: EntityVerificationSessionStatusLiterals
    type: EntityVerificationSessionTypeLiterals
    method: EntityVerificationSessionMethodsLiterals
    sms: Optional[EntityPhoneSmsVerification]
    sna: Optional[EntityPhoneSnaVerification]
    byo_sms: Optional[EntityPhoneSmsVerification]
    byo_kyc: Optional[EntityByoKycVerification]
    kba: Optional[EntityKbaVerification]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityVerificationSessionResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityVerificationSessionResource, self).__init__(config.add_path('verification_sessions'))

    def retrieve(self, verification_session_id: str) -> MethodResponse[EntityVerificationSession]:
        return super(EntityVerificationSessionResource, self)._get_with_id(verification_session_id)

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[EntityVerificationSession]]:
        return super(EntityVerificationSessionResource, self)._list(params)

    def create(self, opts: Optional[EntityVerificationSessionCreateOpts] = {}) -> MethodResponse[EntityVerificationSession]:  # pylint: disable=dangerous-default-value
        return super(EntityVerificationSessionResource, self)._create(opts)

    def update(self, verification_session_id: str, opts: EntityVerificationSessionUpdateOpts) -> MethodResponse[EntityVerificationSession]:
        return super(EntityVerificationSessionResource, self)._update_with_id(verification_session_id, opts)
