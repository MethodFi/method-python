from typing import TypedDict, Optional, List, Literal


PlaidTransactionTypesLiterals = Literal[
    'digital',
    'place',
    'special',
    'unresolved'
]


PlaidTransactionPaymentChannelTypesLiterals = Literal[
    'online',
    'in_store',
    'other'
]


PlaidTransactionCodeLiterals = Literal[
    'adjustment',
    'atm',
    'bank charge',
    'bill payment',
    'cash',
    'cashback',
    'cheque',
    'direct debit',
    'interest',
    'purchase',
    'standing order',
    'transfer',
    'null'
]


PlaidCounterpartyTypeLiterals = Literal[
    'merchant',
    'financial_institution',
    'payment_app',
    'marketplace',
    'payment_terminal',
    'income_source'
]


class PlaidBalance(TypedDict):
    available: Optional[int]
    current: Optional[int]
    iso_currency_code: Optional[str]
    limit: Optional[int]
    unofficial_currency_code: Optional[str]


class PlaidLocation(TypedDict):
    address: Optional[str]
    city: Optional[str]
    region: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    lat: Optional[int]
    lon: Optional[int]
    store_number: Optional[str]


class PlaidPaymentMeta(TypedDict):
    reference_number: Optional[str]
    ppd_id: Optional[str]
    payee: Optional[str]
    by_order_of: Optional[str]
    payer: Optional[str]
    payment_method: Optional[str]
    payment_processor: Optional[str]
    reason: Optional[str]


class PlaidPersonalFinanceCategory(TypedDict):
    primary: str
    detailed: str
    confidence_level: Optional[str]


class PlaidTransactionCounterparty(TypedDict):
    name: str
    entity_id: Optional[str]
    type: PlaidCounterpartyTypeLiterals
    website: Optional[str]
    logo_url: Optional[str]
    confidence_level: Optional[str]


class PlaidTransaction(TypedDict):
    account_id: str
    amount: int
    iso_currency_code: Optional[str]
    unofficial_currency_code: Optional[str]
    category: Optional[List[str]]
    category_id: Optional[str]
    check_number: Optional[str]
    date: str
    location: PlaidLocation
    name: str
    merchant_name: Optional[str]
    original_description: Optional[str]
    payment_meta: PlaidPaymentMeta
    pending: bool
    pending_transaction_id: Optional[str]
    account_owner: Optional[str]
    transaction_id: str
    transaction_type: Optional[PlaidTransactionTypesLiterals]
    logo_url: Optional[str]
    website: Optional[str]
    authorized_date: Optional[str]
    authorized_datetime: Optional[str]
    datetime: Optional[str]
    payment_channel: PlaidTransactionPaymentChannelTypesLiterals
    personal_finance_category: Optional[PlaidPersonalFinanceCategory]
    transaction_code: Optional[PlaidTransactionCodeLiterals]
    personal_finance_category_icon_url: str
    counterparties: List[PlaidTransactionCounterparty]
    merchant_entity_id: Optional[str]


class MXAccount(TypedDict):
    account_number: str
    account_ownership: str
    annuity_policy_to_date: str
    annuity_provider: str
    annuity_term_year: int
    apr: int
    apy: int
    available_balance: int
    available_credit: int
    balance: int
    cash_balance: int
    cash_surrender_value: int
    created_at: str
    credit_limit: int
    currency_code: str
    day_payment_is_due: int
    death_benefit: int
    guid: str
    holdings_value: int
    id: str
    imported_at: str
    interest_rate: int
    institution_code: str
    insured_name: str
    is_closed: bool
    is_hidden: bool
    is_manual: bool
    last_payment: int
    last_payment_at: str
    loan_amount: int
    margin_balance: int
    matures_on: str
    member_guid: str
    member_id: str
    member_is_managed_by_user: bool
    metadata: str
    minimum_balance: int
    minimum_payment: int
    name: str
    nickname: str
    original_balance: int
    pay_out_amount: int
    payment_due_at: str
    payoff_balance: int
    premium_amount: int
    property_type: str
    routing_number: str
    skip_webhook: bool
    started_on: str
    subtype: str
    today_ugl_amount: int
    today_ugl_percentage: int
    total_account_value: int
    type: str
    updated_at: str
    user_guid: str
    user_id: str


class MXTransaction(TypedDict):
    account_guid: str
    account_id: str
    amount: int
    category: str
    category_guid: str
    check_number_string: str
    created_at: str
    currency_code: str
    date: str
    description: str
    extended_transaction_type: str
    guid: str
    id: str
    is_bill_pay: bool
    is_direct_deposit: bool
    is_expense: bool
    is_fee: bool
    is_income: bool
    is_international: bool
    is_overdraft_fee: bool
    is_payroll_advance: bool
    is_recurring: bool
    is_subscription: bool
    latitude: int
    localized_description: str
    localized_memo: str
    longitude: int
    member_guid: str
    member_is_managed_by_user: bool
    memo: str
    merchant_category_code: int
    merchant_guid: str
    merchant_location_guid: str
    metadata: str
    original_description: str
    posted_at: str
    status: str
    top_level_category: str
    transacted_at: str
    type: str
    updated_at: str
    user_guid: str
    user_id: str


class TellerLinks(TypedDict):
    account: str
    self: str


class TellerBalance(TypedDict):
    ledger: int
    links: TellerLinks
    account_id: str
    available: int


class TellerTransactionCounterparty(TypedDict):
    type: str
    name: str


class TellerTransactionDetails(TypedDict):
    category: str
    counterparty: TellerTransactionCounterparty
    processing_status: str


class TellerTransaction(TypedDict):
    running_balance: Optional[int]
    details: TellerTransactionDetails
    description: str
    account_id: str
    date: str
    id: str
    links: TellerLinks
    amount: int
    type: str
    status: str
