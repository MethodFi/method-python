from typing import Literal, Optional, TypedDict

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