from typing import TypedDict, Optional, Literal, List, Any, Dict, Union

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


AccountAttributeBundlesLiterals = Literal[
    'wallet_intelligence',
    'statement',
]


StaticAccountAttributeNamesLiterals = Literal[
    'type',
]


LegacyAccountAttributeNamesLiterals = Literal[
    'debt_settlement',
    'interest_estimate_min',
    'interest_estimate_max',
    'account_standing',
    'delinquent_period',
    'delinquent_amount',
]


AccountRequestableAttributeNamesLiterals = Literal[
    'usage_pattern',
    'delinquency_flag',
    'utilization',
    'utilization_trend_30d',
    'utilization_trend_90d',
    'utilization_delta_30d',
    'utilization_delta_60d',
    'utilization_delta_90d',
    'monthly_installments_estimate',
    'heloc_utilization',
    'available_credit_limit',
    'available_loan_amount',
    'any_delinquent_flag',
    'serious_delinquent_flag',
    'delinquency_recently_cured_flag',
    'delinquency_worst_dpd_bucket',
    'delinquency_progression_flag',
    'delinquent_outcome',
    'next_payment_due_date',
    'next_payment_minimum_amount',
    'estimated_apr',
    'utilization_bucket',
    'purchasing_power',
    'account_age',
    'utilization_velocity_4_week',
    'utilization_velocity_8_week',
    'utilization_velocity_12_week',
    'weeks_since_last_activity',
    'recent_balance_spike_flag',
    'spend_concentration_4_week',
    'spend_concentration_8_week',
    'spend_concentration_12_week',
    'current_wallet_rank',
    'brand_category',
    'brand_tier',
    'enrolled_in_direct_pay_previously',
    'last_direct_pay_date',
    'last_direct_pay_amount',
    'number_of_direct_pay_in_12_months',
]


AccountAttributeNamesLiterals = Literal[
    AccountRequestableAttributeNamesLiterals,
    LegacyAccountAttributeNamesLiterals,
    StaticAccountAttributeNamesLiterals
]


class AccountAttribute(TypedDict):
    value: Any
    error: Optional[ResourceError]
    metadata: Optional[Dict[str, Any]]


class AccountAttributesType(TypedDict):
    type: Optional[AccountAttribute]
    usage_pattern: Optional[AccountAttribute]
    delinquency_flag: Optional[AccountAttribute]
    utilization: Optional[AccountAttribute]
    utilization_trend_30d: Optional[AccountAttribute]
    utilization_trend_90d: Optional[AccountAttribute]
    utilization_delta_30d: Optional[AccountAttribute]
    utilization_delta_60d: Optional[AccountAttribute]
    utilization_delta_90d: Optional[AccountAttribute]
    monthly_installments_estimate: Optional[AccountAttribute]
    heloc_utilization: Optional[AccountAttribute]
    available_credit_limit: Optional[AccountAttribute]
    available_loan_amount: Optional[AccountAttribute]
    any_delinquent_flag: Optional[AccountAttribute]
    serious_delinquent_flag: Optional[AccountAttribute]
    delinquency_recently_cured_flag: Optional[AccountAttribute]
    delinquency_worst_dpd_bucket: Optional[AccountAttribute]
    delinquency_progression_flag: Optional[AccountAttribute]
    delinquent_outcome: Optional[AccountAttribute]
    next_payment_due_date: Optional[AccountAttribute]
    next_payment_minimum_amount: Optional[AccountAttribute]
    estimated_apr: Optional[AccountAttribute]
    utilization_bucket: Optional[AccountAttribute]
    purchasing_power: Optional[AccountAttribute]
    account_age: Optional[AccountAttribute]
    utilization_velocity_4_week: Optional[AccountAttribute]
    utilization_velocity_8_week: Optional[AccountAttribute]
    utilization_velocity_12_week: Optional[AccountAttribute]
    weeks_since_last_activity: Optional[AccountAttribute]
    recent_balance_spike_flag: Optional[AccountAttribute]
    spend_concentration_4_week: Optional[AccountAttribute]
    spend_concentration_8_week: Optional[AccountAttribute]
    spend_concentration_12_week: Optional[AccountAttribute]
    current_wallet_rank: Optional[AccountAttribute]
    brand_category: Optional[AccountAttribute]
    brand_tier: Optional[AccountAttribute]
    enrolled_in_direct_pay_previously: Optional[AccountAttribute]
    last_direct_pay_date: Optional[AccountAttribute]
    last_direct_pay_amount: Optional[AccountAttribute]
    number_of_direct_pay_in_12_months: Optional[AccountAttribute]
    debt_settlement: Optional[AccountAttribute]
    interest_estimate_min: Optional[AccountAttribute]
    interest_estimate_max: Optional[AccountAttribute]
    account_standing: Optional[AccountAttribute]
    delinquent_period: Optional[AccountAttribute]
    delinquent_amount: Optional[AccountAttribute]


AccountAttributesStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


class AccountAttributesCreateOpts(TypedDict):
    requested_attributes: Optional[List[AccountRequestableAttributeNamesLiterals]]
    bundles: Optional[List[AccountAttributeBundlesLiterals]]


class AccountAttributeRequestedAttributesScope(TypedDict):
    requested_attributes: List[AccountRequestableAttributeNamesLiterals]
    bundles: Optional[List[AccountAttributeBundlesLiterals]]


class AccountAttributeBundlesScope(TypedDict):
    requested_attributes: Optional[List[AccountRequestableAttributeNamesLiterals]]
    bundles: List[AccountAttributeBundlesLiterals]


AccountAttributeRequestScope = Union[AccountAttributeRequestedAttributesScope, AccountAttributeBundlesScope]


class AccountAttributes(TypedDict):
    id: str
    account_id: str
    status: AccountAttributesStatusesLiterals
    payload: Optional[Dict[str, Any]]
    attributes: Optional[AccountAttributesType]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountAttributesResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountAttributesResource, self).__init__(config.add_path('attributes'))

    def retrieve(self, acc_attr_id: str) -> MethodResponse[AccountAttributes]:
        return super(AccountAttributesResource, self)._get_with_id(acc_attr_id)

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountAttributes]]:
        return super(AccountAttributesResource, self)._list(params)

    def create(self, opts: Optional[AccountAttributesCreateOpts] = None) -> MethodResponse[AccountAttributes]:
        return super(AccountAttributesResource, self)._create(opts or {})
