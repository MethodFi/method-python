from typing import TypedDict, Optional, Dict, List, Any, Literal

from method.resource import Resource, RequestOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Verification import VerificationResource


AccountTypesLiterals = Literal[
    'ach',
    'liability',
    'clearing'
]


AccountSubTypes = Literal[
    'checking',
    'savings'
]


AccountCapabilitiesLiterals = Literal[
    'payments:receive',
    'payments:send',
    'data:retrieve'
]


AccountStatusesLiterals = Literal[
    'active',
    'disabled',
    'closed',
    'processing'
]

AccountDetailTypesLiterals = Literal[
    'bnpl_loan',
    'depository',
    'credit_card',
    'student_loan'
]


class AccountACH(TypedDict):
    routing: int
    number: int
    type: AccountSubTypes


class AccountLiability(TypedDict):
    mch_id: str
    mask: str


class AccountClearing(TypedDict):
    routing: int
    number: int


class AccountLiabilityCreateOpts(TypedDict):
    mch_id: str
    account_number: str


class Account(TypedDict):
    id: str
    holder_id: str
    status: AccountStatusesLiterals
    type: AccountTypesLiterals
    ach: Optional[AccountACH]
    liability: Optional[AccountLiability]
    clearing: Optional[AccountClearing]
    capabilities: List[AccountCapabilitiesLiterals]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str
    metadata: Optional[Dict[str, Any]]


class AccountCreateOpts(TypedDict):
    holder_id: str
    ach: Optional[AccountACH]
    liability: Optional[AccountLiabilityCreateOpts]
    metadata: Optional[Dict[str, Any]]


class AccountDetailBNPLLoanUpcomingPaymentDue(TypedDict):
    amount: int
    date: str


class AccountDetailBNPLLoan(TypedDict):
    name: Optional[str]
    reference_id: str
    balance: int
    purchase_date: str
    next_payment_due_date: Optional[str]
    total_payments_count: int
    payments_made_count: int
    remaining_payments_count: int
    autopay_enabled: bool
    payoff_progress: int
    interest_rate: int
    description: Optional[str]
    total_cost: int
    total_paid: int
    status: Literal['paid_off', 'refunded', 'in_progress']
    upcoming_payments_due: List[AccountDetailBNPLLoanUpcomingPaymentDue]


class AccountDetailDepository(TypedDict):
    name: Optional[str]
    reference_number: str
    balance: int


class AccountDetailCreditCard(TypedDict):
    name: Optional[str]
    reference_number: str
    balance: int
    last_payment_amount: int
    last_payment_date: Optional[str]
    next_payment_due_date: Optional[str]
    next_payment_minimum_amount: int


# TODO[mdelcarmen]
class AccountDetailStudentLoan(TypedDict):
    pass


class AccountDetail(TypedDict):
    type: AccountDetailTypesLiterals
    bnpl_loan: Optional[AccountDetailBNPLLoan]
    depository: Optional[AccountDetailDepository]
    credit_card: Optional[AccountDetailCreditCard]
    student_loan: Optional[AccountDetailStudentLoan]


class AccountTransaction(TypedDict):
    id: str
    reference_id: str
    date: str
    amount: int
    status: Literal['pending', 'success']
    description: Optional[str]


class AccountListOpts(TypedDict):
    to_date: Optional[str]
    from_date: Optional[str]
    page: Optional[int]
    page_limit: Optional[int]
    page_cursor: Optional[str]
    status: Optional[str]
    type: Optional[str]
    holder_id: Optional[str]


class AccountSubResources:
    verification: VerificationResource

    def __init__(self, _id: str, config: Configuration):
        self.verification = VerificationResource(config.add_path(_id))


class AccountResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountResource, self).__init__(config.add_path('accounts'))

    def __call__(self, _id: str) -> AccountSubResources:
        return AccountSubResources(_id, self.config)

    def get(self, _id: str) -> Account:
        return super(AccountResource, self)._get_with_id(_id)

    def list(self, params: Optional[AccountListOpts] = None) -> List[Account]:
        return super(AccountResource, self)._list(params)

    def create(self, opts: AccountCreateOpts, request_opts: Optional[RequestOpts] = None) -> Account:
        return super(AccountResource, self)._create(opts, request_opts)

    def get_detail(self, _id: str) -> AccountDetail:
        return super(AccountResource, self)._get_with_sub_path('{_id}/detail'.format(_id=_id))

    def get_transactions(self, _id: str) -> List[AccountTransaction]:
        return super(AccountResource, self)._get_with_sub_path('{_id}/transactions'.format(_id=_id))
