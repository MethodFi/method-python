from typing import TypedDict, Optional, Literal, List, Dict

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Accounts.Types import AccountLiabilityTypesLiterals


UserEventTypeLiterals = Literal[
  'AUTH_INTRO_OPEN',
  'AUTH_INTRO_CONTINUE',
  'AUTH_INTRO_CLOSE',

  'AUTH_NAME_OPEN',
  'AUTH_NAME_CONTINUE',
  'AUTH_NAME_CLOSE',

  'AUTH_PHONE_OPEN',
  'AUTH_PHONE_CONTINUE',
  'AUTH_PHONE_CLOSE',

  'AUTH_PHONE_VERIFY_OPEN',
  'AUTH_PHONE_VERIFY_SUBMIT',
  'AUTH_PHONE_VERIFY_RESEND_CODE',
  'AUTH_PHONE_VERIFY_CLOSE',

  'AUTH_DOB_OPEN',
  'AUTH_DOB_CONTINUE',
  'AUTH_DOB_CLOSE',

  'AUTH_ADDRESS_OPEN',
  'AUTH_ADDRESS_CONTINUE',
  'AUTH_ADDRESS_CLOSE',

  'AUTH_SSN4_OPEN',
  'AUTH_SSN4_CONTINUE',
  'AUTH_SSN4_CLOSE',

  'AUTH_SECQ_OPEN',
  'AUTH_SECQ_CONTINUE',
  'AUTH_SECQ_CLOSE',
  'AUTH_SECQ_INCORRECT_TRY_AGAIN',

  'AUTH_CONSENT_OPEN',
  'AUTH_CONSENT_CONTINUE',
  'AUTH_CONSENT_CLOSE',

  'AUTH_SUCCESS_OPEN',
  'AUTH_SUCCESS_CONTINUE',

  'AUTH_FAILURE_OPEN',
  'AUTH_FAILURE_CONTINUE',

  'AVF_ACCOUNT_LIST_OPEN',
  'AVF_ACCOUNT_LIST_CLOSE',

  'AVF_LEARN_MORE_OPEN',
  'AVF_LEARN_MORE_CLOSE',

  'AVF_ACCOUNT_VERIFY_OPEN',
  'AVF_ACCOUNT_VERIFY_SUBMIT',
  'AVF_ACCOUNT_VERIFY_CLOSE',

  'AVF_SUCCESS_OPEN',
  'AVF_SUCCESS_CONTINUE',

  'AVF_EMPTY_SUCCESS_OPEN',
  'AVF_EMPTY_SUCCESS_CONTINUE',

  'AVF_SKIP_ALL',
  'AVF_ERROR',
]


ElementTypesLiterals = Literal[
    'connect',
    'balance_transfer'
]


ElementProducts = Literal[
    'balance',
    'payoff',
    'transactions',
    'card_brand',
    'update',
    'sensitive',
    'payment'
]


ElementMetadataOpTypes = Literal[
    'open',
    'continue',
    'close',
    'success',
    'exit'
]


ElementSelectionTypes = Literal[
    'single',
    'multiple'
]


class ElementUserEvent(TypedDict):
    type: UserEventTypeLiterals
    timestamp: str
    metadata: Optional[Dict[str, any]]


class IndividualOpts(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    dob: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    phone_verification_type: Optional[str]
    phone_verification_timestamp: Optional[str]


class ElementEntityOpts(TypedDict):
    type: Literal['individual']
    individual: IndividualOpts


class ConnectElementFilterOpts(TypedDict):
    selection_type: Optional[ElementSelectionTypes]
    liability_types: Optional[List[AccountLiabilityTypesLiterals]]


class ConnectElementCreateOpts(TypedDict):
    products: Optional[List[ElementProducts]]
    accounts: Optional[List[str]]
    entity: Optional[ElementEntityOpts]
    account_filters: Optional[ConnectElementFilterOpts]


class BalanceTransferElementCreateOpts(TypedDict):
    payment_mount_min: int
    minimum_loan_amount: int
    payout_residual_amount_max: int
    loan_details_requested_amount: int
    loan_details_requested_rate: int
    loan_details_requested_term: int
    loan_details_requested_monthly_payment: int


class ElementTokenCreateOpts(TypedDict):
    entity_id: str
    type: ElementTypesLiterals
    team_name: Optional[str]
    team_logo: Optional[str]
    team_icon: Optional[str]
    connect: Optional[ConnectElementCreateOpts]
    balance_transfer: Optional[BalanceTransferElementCreateOpts]


class ElementToken(TypedDict):
    element_token: str


class ElementMetadata(TypedDict):
    element_type: ElementTypesLiterals
    op: ElementMetadataOpTypes

class ElementResults(TypedDict):
    authenticated: bool
    cxn_id: Optional[str]
    accounts: List[str]
    entity_id: Optional[str]
    events: List[ElementUserEvent]


class ElementTokenResource(Resource):
    def __init__(self, config: Configuration):
        super(ElementTokenResource, self).__init__(config.add_path('token'))

    def create(self, opts: ElementTokenCreateOpts) -> MethodResponse[ElementToken]:
        return super(ElementTokenResource, self)._create(opts)

    def results(self, pk_elem_id: str) -> MethodResponse[ElementResults]:
        return super(ElementTokenResource, self)._get_with_sub_path(
            '{_id}/results'.format(_id=pk_elem_id)
        )
