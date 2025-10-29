from typing import TypedDict, Optional, Literal, List, Dict

from method.resource import MethodResponse, Resource
from method.configuration import Configuration

OpalModesLiterals = Literal[
    'identity_verification',
    'connect',
    'card_connect',
    'account_verification',
    'transactions'
]


SkipPIILiterals = Literal[
    'name',
    'dob',
    'address',
    'ssn_4'
]


class OpalIdentityVerificationCreateOpts(TypedDict):
    skip_pii: List[SkipPIILiterals]


class OpalConnectCreateOpts(TypedDict):
    skip_pii: List[SkipPIILiterals]
    selection_type: Literal['single', 'multiple', 'all']
    allowed_account_types: Literal['credit_card', 'auto_loan', 'mortgage', 'personal_loan', 'student_loan']


class OpalCardConnectCreateOpts(TypedDict):
    skip_pii: List[SkipPIILiterals]
    selection_type: Literal['single', 'multiple', 'all']


class OpalAccountVerificationCreateOpts(TypedDict):
    account_id: str


class OpalTransactionsCreateOpts(TypedDict):
    transactions: Dict[str, any]


class OpalTokenCreateOpts(TypedDict):
    mode: OpalModesLiterals
    entity_id: str
    identity_verification: Optional[OpalIdentityVerificationCreateOpts]
    connect: Optional[OpalConnectCreateOpts]
    card_connect: Optional[OpalCardConnectCreateOpts]
    account_verification: Optional[OpalAccountVerificationCreateOpts]
    transactions: Optional[OpalTransactionsCreateOpts]


class OpalToken(TypedDict):
    token: str
    valid_until: str
    session_id: str


class OpalTokenResource(Resource):
    def __init__(self, config: Configuration):
        super(OpalTokenResource, self).__init__(config.add_path('token'))

    def create(self, opts: OpalTokenCreateOpts) -> MethodResponse[OpalToken]:
        return super(OpalTokenResource, self)._create(opts)
