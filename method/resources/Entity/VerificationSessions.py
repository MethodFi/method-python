from typing import TypedDict, Optional, List, Literal

from method.resource import Resource
from method.configuration import Configuration
from method.errors import ResourceError


EntityVerificationSessionStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


EntityVerificationSessionTypeLiterals = Literal[
    'phone_method_sms',
    'phone_method_sna',
    'phone_byo_sms',
    'identity_byo_kyc',
    'identity_method_kba',
    'identity_method_auth_element'
]


EntityVerificationSessionCategoryLiterals = Literal[
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
    phone_method_sms: Optional[object]
    phone_method_sna: Optional[object]
    phone_byo_sms: Optional[EntityPhoneSmsVerification]
    identity_byo_kyc: Optional[object]
    identity_method_kba: Optional[object]


class EntityVerificationSessionUpdateOpts(TypedDict):
    type: EntityVerificationSessionTypeLiterals
    phone_method_sms: Optional[EntityPhoneSmsVerificationUpdate]
    phone_method_sma: Optional[object]
    identity_method_kba: Optional[EntityKbaVerificationAnswerUpdate]


class EntityVerificationSession(TypedDict):
    id: str
    entity_id: str
    status: EntityVerificationSessionStatusLiterals
    type: EntityVerificationSessionTypeLiterals
    category: EntityVerificationSessionCategoryLiterals
    phone_method_sms: Optional[EntityPhoneSmsVerification]
    phone_method_sna: Optional[EntityPhoneSnaVerification]
    phone_byo_sms: Optional[EntityPhoneSmsVerification]
    identity_byo_kyc: Optional[EntityByoKycVerification]
    identity_method_kba: Optional[EntityKbaVerification]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityVerificationSessionResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityVerificationSessionResource, self).__init__(config.add_path('verification_sessions'))

    def retrieve(self, verification_session_id: str) -> EntityVerificationSession:
        return super(EntityVerificationSessionResource, self)._get_with_id(verification_session_id)

    def create(self, opts: Optional[EntityVerificationSessionCreateOpts] = {}) -> EntityVerificationSession:
        return super(EntityVerificationSessionResource, self)._create(opts)

    def update(self, verification_session_id: str, opts: EntityVerificationSessionUpdateOpts) -> EntityVerificationSession:
        return super(EntityVerificationSessionResource, self)._update_with_id(verification_session_id, opts)
