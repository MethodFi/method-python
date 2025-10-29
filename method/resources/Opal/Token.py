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


AccountFiltersAccountTypesLiterals = Literal[
    'credit_card',
    'auto_loan',
    'mortgage',
    'personal_loan',
    'student_loan'
]


SelectionTypeLiterals = Literal['single', 'multiple', 'all']


class OpalAccountFiltersInclude(TypedDict):
    account_types: List[AccountFiltersAccountTypesLiterals]


class OpalAccountFiltersExclude(TypedDict):
    account_types: List[AccountFiltersAccountTypesLiterals]
    mch_ids: List[str]
    unverified_account_numbers: bool


class ConnectAccountFilters(TypedDict):
    include: OpalAccountFiltersInclude
    exclude: OpalAccountFiltersExclude


class CardConnectAccountFiltersExclude(TypedDict):
    mch_ids: List[str]
    unverified_account_numbers: bool


class CardConnectAccountFilters(TypedDict):
    exclude: CardConnectAccountFiltersExclude


class OpalIdentityVerificationCreateOpts(TypedDict):
    skip_pii: List[SkipPIILiterals]


class OpalConnectCreateOpts(TypedDict):
    skip_pii: List[SkipPIILiterals]
    selection_type: SelectionTypeLiterals
    account_filters: ConnectAccountFilters


class OpalCardConnectCreateOpts(TypedDict):
    skip_pii: List[SkipPIILiterals]
    selection_type: SelectionTypeLiterals
    account_filters: CardConnectAccountFilters


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
