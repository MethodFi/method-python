from typing import TypedDict, Optional, Dict, List, Any, Literal, Union

from method.resource import Resource, RequestOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Accounts import AccountBalance, AccountBalancesResource, AccountCardBrand, AccountCardBrandsResource, \
    AccountPayoff, AccountPayoffsResource, AccountSensitive, AccountSensitiveResource, AccountSubscription, AccountSubscriptionsResource, \
    AccountTransaction, AccountTransactionsResource, AccountUpdate, AccountUpdatesResource, AccountVerificationSession, AccountVerificationSessionResource


AccountLiabilityDataSourcesLiterls = Literal[
    'credit_report',
    'financial_institution',
    'unavailable'
]


AccountLiabilityDataStatusesLiterals = Literal[
    'active',
    'syncing',
    'unavailable',
    'failed',
    'pending'
]


AccountProductTypesLiterals = Literal[
    'payment',
    'balance',
    'sensitive',
    'card_brand',
    'payoff',
    'update'
]


AccountSubscriptionTypesLiterals = Literal[
    'transactions',
    'update',
    'update.snapshot'
]


AccountLiabilityTypesLiterals = Literal[
    'student_loans',
    'credit_card',
    'mortgage',
    'auto_loan',
    'collection',
    'personal_loan',
    'business_loan',
    'insurance',
    'credit_builder',
    'subscription',
    'utility',
    'medical',
    'loan'
]


AccountStatusesLiterals = Literal[
    'active',
    'disabled',
    'closed',
    'processing'
]


AccountTypesLiterals = Literal[
    'ach',
    'liability'
]


TradelineAccountOwnershipLiterals = Literal[
    'primary',
    'authorized',
    'joint',
    'unknown'
]


AccountInterestRateTypesLiterals = Literal[
    'fixed',
    'variable'
]


AccountInterestRateSourcesLiterals = Literal[
    'financial_institution',
    'public_data',
    'method'
]


AchAccountSubTypesLiterals = Literal[
    'checking',
    'savings'
]


AccountLiabilityAutoLoanSubTypesLiterals = Literal[
    'lease',
    'loan'
]


AccountLiabilityCreditCardSubTypesLiterals = Literal[
    'flexible_spending',
    'charge',
    'secured',
    'unsecured',
    'purchase',
    'business'
]


AccountLiabilityCreditCardUsageTypesLiterals = Literal[
    'transactor',
    'revolver',
    'dormant',
    'unknown'
]


AccountLiabilityPersonalLoanSubTypesLiterals = Literal[
    'secured',
    'unsecured',
    'note',
    'line_of_credit',
    'heloc'
]


AccountLiabilityStudentLoanSubTypesLiterals = Literal[
    'federal',
    'private'
]


AccountLiabilityMortgageSubTypesLiterals = Literal[
    'loan'
]


class AccountLiabilityBase(TypedDict):
    balance: Optional[int]
    closed_at: Optional[str]
    last_payment_amount: Optional[int]
    last_payment_date: Optional[str]
    next_payment_due_date: Optional[str]
    next_payment_minimum_amount: Optional[int]
    opened_at: Optional[str]


class AccountLiabilityLoanBase(AccountLiabilityBase):
    expected_payoff_date: Optional[str]
    interest_rate_percentage: Optional[float]
    interest_rate_source: Optional[AccountInterestRateSourcesLiterals]
    interest_rate_type: Optional[AccountInterestRateTypesLiterals]
    original_loan_amount: Optional[int]
    term_length: Optional[int]


class AccountLiabilityAutoLoan(AccountLiabilityLoanBase):
    sub_type: Optional[AccountLiabilityAutoLoanSubTypesLiterals]


class AccountLiabilityCreditCard(AccountLiabilityBase):
    available_credit: Optional[int]
    credit_limit: Optional[int]
    interest_rate_percentage_max: Optional[float]
    interest_rate_percentage_min: Optional[float]
    interest_rate_type: Optional[AccountInterestRateTypesLiterals]
    sub_type: Optional[AccountLiabilityCreditCardSubTypesLiterals]
    usage_pattern: Optional[AccountLiabilityCreditCardUsageTypesLiterals]


class AccountLiabilityMortgage(AccountLiabilityLoanBase):
    sub_type: Optional[AccountLiabilityMortgageSubTypesLiterals]


class AccountLiabilityPersonalLoan(AccountLiabilityLoanBase):
    sub_type: Optional[AccountLiabilityPersonalLoanSubTypesLiterals]
    available_credit: Optional[int]
    

class AccountLiabilityStudentLoansDisbursement(AccountLiabilityLoanBase):
    sequence: int
    disbursed_at: Optional[str]


class AccountLiabilityStudentLoans(AccountLiabilityBase):
    disbursements: Optional[AccountLiabilityStudentLoansDisbursement]
    sub_type: Optional[AccountLiabilityStudentLoanSubTypesLiterals]
    original_loan_amount: Optional[int]
    term_length: Optional[int]


class AccountACH(TypedDict):
    routing: int
    number: int
    type: AchAccountSubTypesLiterals


class AccountLiability(TypedDict):
    mch_id: str
    mask: Optional[str]
    ownership: Optional[TradelineAccountOwnershipLiterals]
    fingerprint: Optional[str]
    type: Optional[AccountLiabilityTypesLiterals]
    name: Optional[str]


class AccountCreateOpts(TypedDict):
    holder_id: str
    metadata: Optional[Dict[str, Any]]


class AccountACHCreateOpts(AccountCreateOpts):
    ach: AccountACH


class LiabilityCreateOpts(TypedDict):
    mch_id: str
    account_number: Optional[str]
    number: Optional[str]


class AccountLiabilityCreateOpts(AccountCreateOpts):
    liability: LiabilityCreateOpts


class Account(TypedDict):
    id: str
    holder_id: str
    status: AccountStatusesLiterals
    type: AccountTypesLiterals
    ach: Optional[AccountACH]
    liability: Optional[AccountLiability]
    products: List[AccountProductTypesLiterals]
    restricted_products: List[AccountProductTypesLiterals]
    subscriptions: Optional[List[AccountSubscriptionTypesLiterals]]
    available_subscriptions: Optional[List[AccountSubscriptionTypesLiterals]]
    restricted_subscriptions: Optional[List[AccountSubscriptionTypesLiterals]]
    sensitive: Optional[Union[str, AccountSensitive]]
    balance: Optional[Union[str, AccountBalance]]
    card_brand: Optional[Union[str, AccountCardBrand]]
    payoff: Optional[Union[str, AccountPayoff]]
    transaction: Optional[Union[str, AccountTransaction]]
    update: Optional[Union[str, AccountUpdate]]
    latest_verification_session: Optional[Union[str, AccountVerificationSession]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str
    metadata: Optional[Dict[str, Any]]


AccountListOpts = TypedDict('AccountListOpts', {
    'to_date': Optional[str],
    'from_date': Optional[str],
    'page': Optional[int],
    'page_limit': Optional[int],
    'page_cursor': Optional[str],
    'status': Optional[str],
    'type': Optional[str],
    'holder_id': Optional[str],
    'liability.mch_id': Optional[str],
    'liability.type': Optional[str]
})


class AccountWithdrawConsentOpts(TypedDict):
    type: Literal['withdraw']
    reason: Optional[Literal['holder_withdrew_consent']]


class AccountSubResources:
    balances: AccountBalancesResource
    card_brands: AccountCardBrandsResource
    payoffs: AccountPayoffsResource
    sensitive: AccountSensitiveResource
    subscriptions: AccountSubscriptionsResource
    transactions: AccountTransactionsResource
    updates: AccountUpdatesResource
    verification_sessions: AccountVerificationSessionResource


    def __init__(self, _id: str, config: Configuration):
        self.balances = AccountBalancesResource(config.add_path(_id))
        self.card_brands = AccountCardBrandsResource(config.add_path(_id))
        self.payoffs = AccountPayoffsResource(config.add_path(_id))
        self.sensitive = AccountSensitiveResource(config.add_path(_id))
        self.subscriptions = AccountSubscriptionsResource(config.add_path(_id))
        self.transactions = AccountTransactionsResource(config.add_path(_id))
        self.updates = AccountUpdatesResource(config.add_path(_id))
        self.verification_sessions = AccountVerificationSessionResource(config.add_path(_id))


class AccountResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountResource, self).__init__(config.add_path('accounts'))

    def __call__(self, _id: str) -> AccountSubResources:
        return AccountSubResources(_id, self.config)

    def retrieve(self, _id: str) -> Account:
        return super(AccountResource, self)._get_with_id(_id)

    def list(self, params: Optional[AccountListOpts] = None) -> List[Account]:
        return super(AccountResource, self)._list(params)

    def create(self, opts: Union[AccountACHCreateOpts, AccountLiabilityCreateOpts], request_opts: Optional[RequestOpts] = None) -> Account:
        return super(AccountResource, self)._create(opts, request_opts)

    def withdraw_consent(self, _id: str, data: AccountWithdrawConsentOpts = { 'type': 'withdraw', 'reason': 'holder_withdrew_consent' }) -> Account:
        return super(AccountResource, self)._create_with_sub_path('{_id}/consent'.format(_id=_id), data)

