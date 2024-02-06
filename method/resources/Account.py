from typing import TypedDict, Optional, Dict, List, Any, Literal, Union

from method.resource import Resource, RequestOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Verification import VerificationResource
from method.resources.AccountSync import AccountSyncResource, AccountSync


# Literals, keep ordered alphabetically
AccountCapabilitiesLiterals = Literal[
    'payments:receive',
    'payments:send',
    'data:retrieve',
    'data:sync'
]


AccountClearingSubTypesLiterals = Literal[
    'single_use'
]


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


AccountLiabilityPaymentStatuesLiterals = Literal[
    'active',
    'activating',
    'unavailable'
]


AccountLiabilitySyncTypesLiterals = Literal[
    'manual',
    'auto'
]


AccountLiabilityTypesLiterals = Literal[
    'student_loan',
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


AccountSubTypesLiterals = Literal[
    'checking',
    'savings'
]


AccountTypesLiterals = Literal[
    'ach',
    'liability',
    'clearing'
]

AutoPayStatusesLiterals = Literal[
    'unknown',
    'active',
    'inactive'
]


TradelineAccountOwnershipLiterals = Literal[
    'primary',
    'authorized',
    'joint',
    'unknown'
]


PastDueStatusesLiterals = Literal[
    'unknown',
    'overdue',
    'on_time'
]


DelinquencyStatusLiterals = Literal[
    'good_standing',
    'past_due',
    'major_delinquency',
    'unavailable'
]


DelinquencyPeriodLiterals = Literal[
    'less_than_30',
    '30',
    '60',
    '90',
    '120',
    'over_120'
]

AccountPayoffStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]

class AccountACH(TypedDict):
    routing: int
    number: int
    type: AccountSubTypesLiterals


class AccountLiabilityLoan(TypedDict):
    name: str
    balance: Optional[int]
    opened_at: Optional[str]
    original_loan_amount: Optional[int]
    sub_type: Optional[str]
    term_length: Optional[int]
    closed_at: Optional[str]
    last_payment_amount: Optional[int]
    last_payment_date: Optional[str]
    next_payment_minimum_amount: Optional[int]
    next_payment_due_date: Optional[str]
    interest_rate_type: Literal['fixed', 'variable']
    interest_rate_percentage: Optional[int]
    interest_rate_source: Optional[Literal['financial_institution', 'public_data', 'method']]


class AccountLiabilityCreditCard(AccountLiabilityLoan):
    last_statement_balance: Optional[int]
    remaining_statement_balance: Optional[int]
    available_credit: Optional[int]
    auto_pay_status: Optional[AutoPayStatusesLiterals]
    auto_pay_amount: Optional[int]
    auto_pay_date: Optional[str]
    past_due_status: Optional[PastDueStatusesLiterals]
    past_due_balance: Optional[int]
    past_due_date: Optional[str]
    credit_limit: Optional[int]
    pending_purchase_authorization_amount: Optional[int]
    pending_credit_authorization_amount: Optional[int]
    interest_saving_balance: Optional[int]
    next_statement_date: Optional[str]


class AccountLiabilityAutoLoan(AccountLiabilityLoan):
    sub_type: Optional[Literal['lease', 'loan']]
    payoff_amount: Optional[int]
    payoff_amount_term: Optional[int]
    past_due_status: Optional[PastDueStatusesLiterals]
    past_due_balance: Optional[int]
    past_due_date: Optional[str]
    late_fees_amount: Optional[int]
    expected_payoff_date: Optional[str]
    principal_balance: Optional[int]
    per_diem_amount: Optional[int]
    mileage_allocation: Optional[int]


class AccountLiabilityStudentLoan(AccountLiabilityLoan):
    sub_type: Optional[Literal['federal', 'private']]
    sequence: Optional[int]
    disbursed_at: Optional[str]
    expected_payoff_date: Optional[str]
    payoff_amount: Optional[int]
    payoff_amount_term: Optional[int]
    principal_balance: Optional[int]
  

class DelinquencyHistoryItem(TypedDict):
    start_date: str
    end_date: str
    status: DelinquencyStatusLiterals
    period: Optional[DelinquencyPeriodLiterals]
  

class TrendedDataItem(TypedDict):
    month: Optional[int]
    year: Optional[int]
    balance: Optional[int]
    available_credit: Optional[int]
    scheduled_payment: Optional[int]
    actual_payment: Optional[int]
    high_credit: Optional[int]
    credit_limit: Optional[int]
    amount_past_due: Optional[int]
    last_payment_date: Optional[str]
    account_status: str
    payment_status:str
    

class AccountLiabilityStudentLoansDisbursement(AccountLiabilityLoan):
    sequence: int
    disbursed_at: Optional[str]
    expected_payoff_date: Optional[str]
    delinquent_status: Optional[str]
    delinquent_amount: Optional[int]
    delinquent_period: Optional[int]
    delinquent_action: Optional[str]
    delinquent_start_date: Optional[str]
    delinquent_major_start_date: Optional[str]
    delinquent_status_updated_at: Optional[str]
    delinquent_history: Optional[List[DelinquencyHistoryItem]]
    delinquent_action: Optional[List[TrendedDataItem]]


class AccountLiabilityStudentLoans(AccountLiabilityLoan):
    sub_type: Optional[Literal['federal', 'private']]
    disbursed_at: Optional[str]
    expected_payoff_date: Optional[str]
    interest_rate_type: Optional[Literal['fixed', 'variable']]
    expected_payoff_date: Optional[str]
    disbursements: Optional[AccountLiabilityStudentLoansDisbursement]


class AccountLiabilityMortgage(AccountLiabilityLoan):
    principal_balance: Optional[int]
    expected_payoff_date: Optional[str]
    address_street: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    address_zip: Optional[str]
    property_value: Optional[int]
    past_due_status: Optional[PastDueStatusesLiterals]
    past_due_balance: Optional[int]
    past_due_date: Optional[str]
    payoff_amount: Optional[int]
    payoff_amount_term: Optional[int]
    year_to_date_interest_paid: Optional[int]
    year_to_date_principal_paid: Optional[int]
    year_to_date_taxes_paid: Optional[int]
    year_start_principal_balance: Optional[int]
    escrow_balance: Optional[int]


class AccountLiabilityPersonalLoan(AccountLiabilityLoan):
    expected_payoff_date: Optional[str]
    available_credit: Optional[int]
    principal_balance: Optional[int]
    year_to_date_interest_paid: Optional[int]


class AccountLiabilityCreditBuilder(AccountLiabilityLoan):
    pass


class AccountLiabilityCollection(AccountLiabilityLoan):
    pass


class AccountLiabilityBusinessLoan(TypedDict):
    name: str
    balance: Optional[int]
    opened_at: Optional[str]


class AccountLiabilityInsurance(TypedDict):
    name: str
    balance: Optional[int]
    opened_at: Optional[str]


class AccountLiabilitySubscription(TypedDict):
    name: str
    balance: Optional[int]
    opened_at: Optional[str]


class AccountLiabilityUtility(TypedDict):
    name: str
    balance: Optional[int]
    opened_at: Optional[str]


class AccountLiabilityMedical(TypedDict):
    name: str
    balance: Optional[int]
    opened_at: Optional[str]


class AccountLiability(TypedDict):
    mch_id: str
    mask: str
    payment_status: AccountLiabilityPaymentStatuesLiterals
    data_status: AccountLiabilityDataStatusesLiterals
    data_last_successful_sync: Optional[str]
    data_status_error: Optional[ResourceError]
    data_source: AccountLiabilityDataSourcesLiterls
    data_updated_at: Optional[str]
    data_sync_type: AccountLiabilitySyncTypesLiterals
    ownership: TradelineAccountOwnershipLiterals
    hash: str
    fingerprint: str
    type: AccountLiabilityTypesLiterals
    loan: Optional[AccountLiabilityLoan]
    student_loan: Optional[AccountLiabilityStudentLoan]
    student_loans: Optional[AccountLiabilityStudentLoans]
    credit_card: Optional[AccountLiabilityCreditCard]
    mortgage: Optional[AccountLiabilityMortgage]
    auto_loan: Optional[AccountLiabilityAutoLoan]
    personal_loan: Optional[AccountLiabilityPersonalLoan]
    business_loan: Optional[AccountLiabilityBusinessLoan]
    collection: Optional[AccountLiabilityCollection]
    insurance: Optional[AccountLiabilityInsurance]
    credit_builder: Optional[AccountLiabilityCreditBuilder]
    subscription: Optional[AccountLiabilitySubscription]
    utility: Optional[AccountLiabilityUtility]
    medical: Optional[AccountLiabilityMedical]


class AccountClearing(TypedDict):
    routing: int
    number: int


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


class ClearingCreateOpts(TypedDict):
    type: AccountClearingSubTypesLiterals


class AccountClearingCreateOpts(AccountCreateOpts):
    clearing: ClearingCreateOpts


class Account(TypedDict):
    id: str
    holder_id: str
    status: AccountStatusesLiterals
    type: AccountTypesLiterals
    ach: Optional[AccountACH]
    liability: Optional[AccountLiability]
    clearing: Optional[AccountClearing]
    capabilities: List[AccountCapabilitiesLiterals]
    available_capabilities: List[AccountCapabilitiesLiterals]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str
    metadata: Optional[Dict[str, Any]]


class AccountDetail(TypedDict):
    id: str
    type: AccountTypesLiterals
    aggregator: Optional[str]
    name: str
    institution_name: str
    institution_logo: str
    mask: str
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


class AccountCreateBulkSyncOpts(TypedDict):
    acc_ids: List[str]


class AccountCreateBulkSyncResponse(TypedDict):
    success: List[str]
    failed: List[str]
    results: List[AccountSync]


class AccountSensitive(TypedDict):
    number: Optional[str]
    encrypted_number: Optional[str]
    bin_4: Optional[str]
    bin_6: Optional[str]
    payment_address: Optional[Any]


class AccountCreateBulkSensitiveResponse(TypedDict):
    success: List[str]
    failed: List[str]
    results: List[AccountSensitive]


class AccountCreateBulkSensitiveOpts(TypedDict):
    acc_ids: List[str]


class AccountWithdrawConsentOpts(TypedDict):
    type: Literal['withdraw']
    reason: Optional[Literal['holder_withdrew_consent']]


class LiabilityMortgageUpdateOpts(TypedDict):
    address_street: str
    address_city: str
    address_state: str
    address_zip: str


class LiabilityCreditCardUpdateNumberOpts(TypedDict):
    number: str


class LiabilityCreditCardUpdateExpirationOpts(TypedDict):
    expiration_month: int
    expiration_year: int


class LiabilityUpdateOpts(TypedDict):
    mortgage: Optional[LiabilityMortgageUpdateOpts]
    credit_card: Union[LiabilityCreditCardUpdateNumberOpts, LiabilityCreditCardUpdateExpirationOpts]


class CreditReportTradelinePaymentHistoryItem(TypedDict):
    code: int
    date: str


class AccountPaymentHistory(TypedDict):
    payment_history: List[CreditReportTradelinePaymentHistoryItem]


class AccountPayoff(TypedDict):
    id: str
    status: AccountPayoffStatusesLiterals
    amount: Optional[int]
    term: Optional[int]
    per_diem_amount: Optional[int]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountSubResources:
    verification: VerificationResource
    sync: AccountSyncResource

    def __init__(self, _id: str, config: Configuration):
        self.verification = VerificationResource(config.add_path(_id))
        self.syncs = AccountSyncResource(config.add_path(_id))

class AccountResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountResource, self).__init__(config.add_path('accounts'))

    def __call__(self, _id: str) -> AccountSubResources:
        return AccountSubResources(_id, self.config)

    def get(self, _id: str) -> Account:
        return super(AccountResource, self)._get_with_id(_id)

    def update(self, _id: str, opts: LiabilityUpdateOpts) -> Account:
        return super(AccountResource, self)._update_with_id(_id, opts)

    def list(self, params: Optional[AccountListOpts] = None) -> List[Account]:
        return super(AccountResource, self)._list(params)

    def create(self, opts: Union[AccountACHCreateOpts, AccountLiabilityCreateOpts, AccountClearingCreateOpts], request_opts: Optional[RequestOpts] = None) -> Account:
        return super(AccountResource, self)._create(opts, request_opts)

    def get_payment_history(self, _id: str) -> AccountPaymentHistory:
        return super(AccountResource, self)._get_with_sub_path('{_id}/payment_history'.format(_id=_id))

    def get_details(self, _id: str) -> AccountDetail:
        return super(AccountResource, self)._get_with_sub_path('{_id}/details'.format(_id=_id))

    def bulk_sync(self, acc_ids: AccountCreateBulkSyncOpts) -> AccountCreateBulkSyncResponse:
        return super(AccountResource, self)._create_with_sub_path('bulk_sync',{ acc_ids })

    def sync(self, _id: str) -> AccountSync:
        return super(AccountResource, self)._create_with_sub_path('{_id}/syncs'.format(_id=_id), {})

    def bulk_sensitive(self, acc_ids: AccountCreateBulkSensitiveOpts) -> AccountCreateBulkSensitiveResponse:
        return super(AccountResource, self)._create_with_sub_path('bulk_sensitive',{ acc_ids })

    def sensitive(self, _id: str) -> AccountSensitive:
        return super(AccountResource, self)._get_with_sub_path('{_id}/sensitive'.format(_id=_id))

    def enroll_auto_syncs(self, _id: str) -> Account:
        return super(AccountResource, self)._create_with_sub_path('{_id}/sync_enrollment'.format(_id=_id), {})

    def unenroll_auto_syncs(self, _id: str) -> Account:
        return super(AccountResource, self)._delete_with_sub_path('{_id}/sync_enrollment'.format(_id=_id))

    def withdraw_consent(self, _id: str, data: AccountWithdrawConsentOpts = { 'type': 'withdraw', 'reason': 'holder_withdrew_consent' }) -> Account:
        return super(AccountResource, self)._create_with_sub_path('{_id}/consent'.format(_id=_id), data)
    
    def get_payoff(self, _id: str, pyf_id: str) -> AccountPayoff:
        return super(AccountResource, self)._get_with_sub_path('{_id}/payoffs/{pyf_id}'.format(_id=_id, pyf_id=pyf_id))
    
    def create_payoff(self, _id: str) -> AccountPayoff:
        return super(AccountResource, self)._create_with_sub_path('{_id}/payoffs'.format(_id=_id), {})
