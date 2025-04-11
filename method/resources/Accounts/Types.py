from typing import Literal, Optional, TypedDict


AccountTypesLiterals = Literal[
    'ach',
    'liability'
]


AccountStatusesLiterals = Literal[
    'active',
    'disabled',
    'closed'
]


AccountProductTypesLiterals = Literal[
    'payment',
    'balance',
    'sensitive',
    'card_brand',
    'payoff',
    'update',
    'attribute',
    'transaction',
    'payment_instrument'
]


AccountSubscriptionTypesLiterals = Literal[
    'card_brand',
    'payment_instrument',
    'transaction',
    'update',
    'update.snapshot'
]


AccountOwnershipLiterals = Literal[
    'primary',
    'authorized',
    'joint',
    'unknown'
]


AccountUpdateSourceLiterals = Literal[
    'direct',
    'snapshot'
]


AccountLiabilityTypesLiterals = Literal[
    'auto_loan',
    'bnpl',
    'credit_builder',
    'credit_card',
    'collection',
    'fintech',
    'insurance',
    'loan',
    'medical',
    'mortgage',
    'personal_loan',
    'student_loans',
    'utility',
]


AchAccountSubTypesLiterals = Literal[
    'checking',
    'savings'
]


AccountExpandableFieldsLiterals = Literal[
    AccountProductTypesLiterals,
    'latest_verification_session'
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


AccountLiabilityMortgageSubTypesLiterals = Literal[
    'loan'
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


class AccountLiabilityCollection(AccountLiabilityBase):
    pass


class AccountLiabilityMortgage(AccountLiabilityLoanBase):
    sub_type: Optional[AccountLiabilityMortgageSubTypesLiterals]


class AccountLiabilityPersonalLoan(AccountLiabilityLoanBase):
    available_credit: Optional[int]
    sub_type: Optional[AccountLiabilityPersonalLoanSubTypesLiterals]
    

class AccountLiabilityStudentLoansDisbursement(AccountLiabilityLoanBase):
    sequence: int
    disbursed_at: Optional[str]


class AccountLiabilityStudentLoans(AccountLiabilityBase):
    disbursements: Optional[AccountLiabilityStudentLoansDisbursement]
    sub_type: Optional[AccountLiabilityStudentLoanSubTypesLiterals]
    original_loan_amount: Optional[int]
    term_length: Optional[int]


class AccountLiability(TypedDict):
    mch_id: str
    mask: Optional[str]
    ownership: Optional[AccountOwnershipLiterals]
    fingerprint: Optional[str]
    type: Optional[AccountLiabilityTypesLiterals]
    name: Optional[str]


class AccountACH(TypedDict):
    routing: int
    number: int
    type: AchAccountSubTypesLiterals
