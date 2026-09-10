from typing import TypedDict, Optional, Literal, List, Any, Dict

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


EntityAttributesResponseStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


EntityAttributeBundlesLiterals = Literal[
    'portfolio_intelligence',
    'wallet_intelligence',
]


LegacyEntityAttributeNamesLiterals = Literal[
    'credit_health_credit_card_usage',
    'credit_health_derogatory_marks',
    'credit_health_hard_inquiries',
    'credit_health_soft_inquiries',
    'credit_health_total_accounts',
    'credit_health_credit_age',
    'credit_health_payment_history',
    'credit_health_open_accounts',
    'credit_health_entity_delinquent',
]


EntityRequestableAttributeNamesLiterals = Literal[
    'revolving_credit_card_balance_total',
    'credit_limit_total',
    'credit_card_utilization',
    'available_credit_limit_total',
    'available_credit_total',
    'weighted_average_apr_credit_card',
    'usage_pattern',
    'utilization',
    'purchasing_power',
    'healthy_cards_count',
    'dormant_cards_count',
    'delinquent_cards_count',
    'net_active_cards_count',
    'utilization_velocity_4_week',
    'utilization_velocity_8_week',
    'utilization_velocity_12_week',
    'next_payment_minimum_total_credit_cards',
    'payment_to_minimum_ratio_avg_credit_cards',
    'revolving_credit_card_balance_change_30d',
    'revolving_credit_card_balance_change_60d',
    'revolving_credit_card_balance_change_90d',
    'revolving_credit_card_utilization_trend_30d',
    'revolving_credit_card_utilization_trend_90d',
    'revolving_credit_card_utilization_delta_30d',
    'revolving_credit_card_utilization_delta_60d',
    'revolving_credit_card_utilization_delta_90d',
    'delinquency_flag_credit_cards',
    'any_delinquent_flag',
    'serious_delinquent_flag',
    'delinquency_recently_cured_flag',
    'delinquency_worst_dpd_bucket',
    'delinquency_accounts_count',
    'delinquent_balance_total',
    'delinquency_progression_flag',
    'delinquent_outcome',
    'personal_loan_balance_total',
    'personal_loan_amount_total',
    'available_loan_amount_personal_loans',
    'personal_loan_monthly_installments_estimate',
    'personal_loan_utilization',
    'weighted_average_apr_personal_loan',
    'personal_loan_balance_change_30d',
    'personal_loan_balance_change_60d',
    'personal_loan_balance_change_90d',
    'personal_loan_utilization_trend_30d',
    'personal_loan_utilization_trend_90d',
    'personal_loan_utilization_delta_30d',
    'personal_loan_utilization_delta_60d',
    'personal_loan_utilization_delta_90d',
    'mortgage_balance_total',
    'mortgage_loan_amount_total',
    'weighted_average_apr_mortgage',
    'mortgage_balance_change_30d',
    'mortgage_balance_change_60d',
    'mortgage_balance_change_90d',
    'mortgage_utilization_trend_30d',
    'mortgage_utilization_trend_90d',
    'mortgage_utilization_delta_30d',
    'mortgage_utilization_delta_60d',
    'mortgage_utilization_delta_90d',
    'heloc_balance_total',
    'heloc_utilization',
    'overall_loan_amount_total',
    'overall_utilization',
    'overall_utilization_trend_30d',
    'overall_utilization_trend_90d',
    'overall_utilization_delta_30d',
    'overall_utilization_delta_60d',
    'overall_utilization_delta_90d',
    'installment_balance_total',
    'installment_balance_change_30d',
    'installment_balance_change_60d',
    'installment_balance_change_90d',
    'other_balance_total',
    'other_balance_change_30d',
    'other_balance_change_60d',
    'other_balance_change_90d',
    'enrolled_in_direct_pay_previously',
    'last_direct_pay_date',
    'last_direct_pay_amount',
    'number_of_direct_pay_in_12_months',
]


EntityAttributeNamesLiterals = Literal[
    EntityRequestableAttributeNamesLiterals,
    LegacyEntityAttributeNamesLiterals
]


CreditHealthAttributeRating = Literal[
    'excellent',
    'good',
    'fair',
    'needs_work'
]


class EntityAttribute(TypedDict):
    value: Any
    error: Optional[ResourceError]
    metadata: Optional[Dict[str, Any]]


class CreditHealthAttribute(TypedDict):
    value: int
    rating: CreditHealthAttributeRating
    metadata: Optional[Dict[str, Any]]


class EntityAttributesType(TypedDict):
    revolving_credit_card_balance_total: Optional[EntityAttribute]
    credit_limit_total: Optional[EntityAttribute]
    credit_card_utilization: Optional[EntityAttribute]
    available_credit_limit_total: Optional[EntityAttribute]
    available_credit_total: Optional[EntityAttribute]
    weighted_average_apr_credit_card: Optional[EntityAttribute]
    usage_pattern: Optional[EntityAttribute]
    utilization: Optional[EntityAttribute]
    purchasing_power: Optional[EntityAttribute]
    healthy_cards_count: Optional[EntityAttribute]
    dormant_cards_count: Optional[EntityAttribute]
    delinquent_cards_count: Optional[EntityAttribute]
    net_active_cards_count: Optional[EntityAttribute]
    utilization_velocity_4_week: Optional[EntityAttribute]
    utilization_velocity_8_week: Optional[EntityAttribute]
    utilization_velocity_12_week: Optional[EntityAttribute]
    next_payment_minimum_total_credit_cards: Optional[EntityAttribute]
    payment_to_minimum_ratio_avg_credit_cards: Optional[EntityAttribute]
    revolving_credit_card_balance_change_30d: Optional[EntityAttribute]
    revolving_credit_card_balance_change_60d: Optional[EntityAttribute]
    revolving_credit_card_balance_change_90d: Optional[EntityAttribute]
    revolving_credit_card_utilization_trend_30d: Optional[EntityAttribute]
    revolving_credit_card_utilization_trend_90d: Optional[EntityAttribute]
    revolving_credit_card_utilization_delta_30d: Optional[EntityAttribute]
    revolving_credit_card_utilization_delta_60d: Optional[EntityAttribute]
    revolving_credit_card_utilization_delta_90d: Optional[EntityAttribute]
    delinquency_flag_credit_cards: Optional[EntityAttribute]
    any_delinquent_flag: Optional[EntityAttribute]
    serious_delinquent_flag: Optional[EntityAttribute]
    delinquency_recently_cured_flag: Optional[EntityAttribute]
    delinquency_worst_dpd_bucket: Optional[EntityAttribute]
    delinquency_accounts_count: Optional[EntityAttribute]
    delinquent_balance_total: Optional[EntityAttribute]
    delinquency_progression_flag: Optional[EntityAttribute]
    delinquent_outcome: Optional[EntityAttribute]
    personal_loan_balance_total: Optional[EntityAttribute]
    personal_loan_amount_total: Optional[EntityAttribute]
    available_loan_amount_personal_loans: Optional[EntityAttribute]
    personal_loan_monthly_installments_estimate: Optional[EntityAttribute]
    personal_loan_utilization: Optional[EntityAttribute]
    weighted_average_apr_personal_loan: Optional[EntityAttribute]
    personal_loan_balance_change_30d: Optional[EntityAttribute]
    personal_loan_balance_change_60d: Optional[EntityAttribute]
    personal_loan_balance_change_90d: Optional[EntityAttribute]
    personal_loan_utilization_trend_30d: Optional[EntityAttribute]
    personal_loan_utilization_trend_90d: Optional[EntityAttribute]
    personal_loan_utilization_delta_30d: Optional[EntityAttribute]
    personal_loan_utilization_delta_60d: Optional[EntityAttribute]
    personal_loan_utilization_delta_90d: Optional[EntityAttribute]
    mortgage_balance_total: Optional[EntityAttribute]
    mortgage_loan_amount_total: Optional[EntityAttribute]
    weighted_average_apr_mortgage: Optional[EntityAttribute]
    mortgage_balance_change_30d: Optional[EntityAttribute]
    mortgage_balance_change_60d: Optional[EntityAttribute]
    mortgage_balance_change_90d: Optional[EntityAttribute]
    mortgage_utilization_trend_30d: Optional[EntityAttribute]
    mortgage_utilization_trend_90d: Optional[EntityAttribute]
    mortgage_utilization_delta_30d: Optional[EntityAttribute]
    mortgage_utilization_delta_60d: Optional[EntityAttribute]
    mortgage_utilization_delta_90d: Optional[EntityAttribute]
    heloc_balance_total: Optional[EntityAttribute]
    heloc_utilization: Optional[EntityAttribute]
    overall_loan_amount_total: Optional[EntityAttribute]
    overall_utilization: Optional[EntityAttribute]
    overall_utilization_trend_30d: Optional[EntityAttribute]
    overall_utilization_trend_90d: Optional[EntityAttribute]
    overall_utilization_delta_30d: Optional[EntityAttribute]
    overall_utilization_delta_60d: Optional[EntityAttribute]
    overall_utilization_delta_90d: Optional[EntityAttribute]
    installment_balance_total: Optional[EntityAttribute]
    installment_balance_change_30d: Optional[EntityAttribute]
    installment_balance_change_60d: Optional[EntityAttribute]
    installment_balance_change_90d: Optional[EntityAttribute]
    other_balance_total: Optional[EntityAttribute]
    other_balance_change_30d: Optional[EntityAttribute]
    other_balance_change_60d: Optional[EntityAttribute]
    other_balance_change_90d: Optional[EntityAttribute]
    enrolled_in_direct_pay_previously: Optional[EntityAttribute]
    last_direct_pay_date: Optional[EntityAttribute]
    last_direct_pay_amount: Optional[EntityAttribute]
    number_of_direct_pay_in_12_months: Optional[EntityAttribute]
    credit_health_credit_card_usage: Optional[CreditHealthAttribute]
    credit_health_derogatory_marks: Optional[CreditHealthAttribute]
    credit_health_hard_inquiries: Optional[CreditHealthAttribute]
    credit_health_soft_inquiries: Optional[CreditHealthAttribute]
    credit_health_total_accounts: Optional[CreditHealthAttribute]
    credit_health_credit_age: Optional[CreditHealthAttribute]
    credit_health_payment_history: Optional[CreditHealthAttribute]
    credit_health_open_accounts: Optional[CreditHealthAttribute]
    credit_health_entity_delinquent: Optional[CreditHealthAttribute]


class EntityAttributesCreateOpts(TypedDict):
    requested_attributes: Optional[List[EntityRequestableAttributeNamesLiterals]]
    bundles: Optional[List[EntityAttributeBundlesLiterals]]


class EntityAttributes(TypedDict):
    id: str
    entity_id: str
    status: EntityAttributesResponseStatusLiterals
    attributes: Optional[EntityAttributesType]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityAttributesResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityAttributesResource, self).__init__(config.add_path('attributes'))

    def retrieve(self, attr_id: str) -> MethodResponse[EntityAttributes]:
        return super(EntityAttributesResource, self)._get_with_id(attr_id)

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[EntityAttributes]]:
        return super(EntityAttributesResource, self)._list(params)

    def create(self, opts: Optional[EntityAttributesCreateOpts] = None) -> MethodResponse[EntityAttributes]:
        return super(EntityAttributesResource, self)._create(opts or {})
