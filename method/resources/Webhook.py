from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resource import MethodResponse, Resource, RequestOpts
from method.configuration import Configuration


WebhookTypesLiterals = Literal[
    'payment.create',
    'payment.update',
    'account.create',
    'account.update',
    'entity.update',
    'entity.create',
    'account_verification.create',
    'account_verification.update',
    'payment_reversal.create',
    'payment_reversal.update',
    'connection.create',
    'connection.update',
    'transaction.create',
    'transaction.update',
    'report.create',
    'report.update',
    'product.create',
    'product.update',
    'subscription.create',
    'subscription.update',
    'credit_score.create',
    'credit_score.update',
    'payoff.create',
    'payoff.update',
    'entity_verification_session.create',
    'entity_verification_session.update',
    'connect.create',
    'connect.update',
    'connect.available',
    'balance.create',
    'balance.update',
    'identity.create',
    'identity.update',
    'account_verification_session.create',
    'account_verification_session.update',
    'card_brand.create',
    'card_brand.update',
    'card_brand.available',
    'sensitive.create',
    'sensitive.update',
    'update.create',
    'update.update',
    'attribute.create',
    'attribute.update',
    'entity_attribute.create',
    'entity_attribute.update',
    'account_attribute.create',
    'account_attribute.update',
    'account.opened',
    'account.closed',
    'credit_score.increased',
    'credit_score.decreased',
    'entity_attribute.credit_health_open_accounts_value.increased',
    'entity_attribute.credit_health_open_accounts_value.decreased',
    'entity_attribute.credit_health_total_accounts_value.increased',
    'entity_attribute.credit_health_total_accounts_value.decreased',
    'entity_attribute.credit_health_credit_card_usage_value.increased',
    'entity_attribute.credit_health_credit_card_usage_value.decreased',
    'entity_attribute.credit_health_soft_inquiries_value.increased',
    'entity_attribute.credit_health_soft_inquiries_value.decreased',
    'entity_attribute.credit_health_hard_inquiries_value.increased',
    'entity_attribute.credit_health_hard_inquiries_value.decreased',
    'entity_attribute.revolving_credit_card_balance_total.increased',
    'entity_attribute.revolving_credit_card_balance_total.decreased',
    'entity_attribute.personal_loan_balance_total.increased',
    'entity_attribute.personal_loan_balance_total.decreased',
    'entity_attribute.revolving_credit_card_balance_change_30d.increased',
    'entity_attribute.revolving_credit_card_balance_change_30d.decreased',
    'entity_attribute.revolving_credit_card_balance_change_60d.increased',
    'entity_attribute.revolving_credit_card_balance_change_60d.decreased',
    'entity_attribute.revolving_credit_card_balance_change_90d.increased',
    'entity_attribute.revolving_credit_card_balance_change_90d.decreased',
    'entity_attribute.personal_loan_balance_change_30d.increased',
    'entity_attribute.personal_loan_balance_change_30d.decreased',
    'entity_attribute.personal_loan_balance_change_60d.increased',
    'entity_attribute.personal_loan_balance_change_60d.decreased',
    'entity_attribute.personal_loan_balance_change_90d.increased',
    'entity_attribute.personal_loan_balance_change_90d.decreased',
    'entity_attribute.usage_pattern.changed',
    'entity_attribute.delinquency_flag_credit_cards.set',
    'entity_attribute.delinquency_flag_credit_cards.cleared',
    'entity_attribute.weighted_average_apr_credit_card.increased',
    'entity_attribute.weighted_average_apr_credit_card.decreased',
    'entity_attribute.weighted_average_apr_personal_loan.increased',
    'entity_attribute.weighted_average_apr_personal_loan.decreased',
    'entity_attribute.credit_card_utilization.increased',
    'entity_attribute.credit_card_utilization.decreased',
    'entity_attribute.personal_loan_utilization.increased',
    'entity_attribute.personal_loan_utilization.decreased',
    'entity_attribute.overall_utilization.increased',
    'entity_attribute.overall_utilization.decreased',
    'entity_attribute.revolving_credit_card_utilization_trend_30d.increased',
    'entity_attribute.revolving_credit_card_utilization_trend_30d.decreased',
    'entity_attribute.personal_loan_utilization_trend_30d.increased',
    'entity_attribute.personal_loan_utilization_trend_30d.decreased',
    'entity_attribute.credit_limit_total.increased',
    'entity_attribute.credit_limit_total.decreased',
    'entity_attribute.personal_loan_amount_total.increased',
    'entity_attribute.personal_loan_amount_total.decreased',
    'entity_attribute.mortgage_loan_amount_total.increased',
    'entity_attribute.mortgage_loan_amount_total.decreased',
    'entity_attribute.overall_loan_amount_total.increased',
    'entity_attribute.overall_loan_amount_total.decreased',
    'entity_attribute.personal_loan_monthly_installments_estimate.increased',
    'entity_attribute.personal_loan_monthly_installments_estimate.decreased',
    'entity_attribute.next_payment_minimum_total_credit_cards.increased',
    'entity_attribute.next_payment_minimum_total_credit_cards.decreased',
    'entity_attribute.payment_to_minimum_ratio_avg_credit_cards.increased',
    'entity_attribute.payment_to_minimum_ratio_avg_credit_cards.decreased',
    'entity_attribute.revolving_credit_card_utilization_trend_90d.increased',
    'entity_attribute.revolving_credit_card_utilization_trend_90d.decreased',
    'entity_attribute.revolving_credit_card_utilization_delta_30d.increased',
    'entity_attribute.revolving_credit_card_utilization_delta_30d.decreased',
    'entity_attribute.revolving_credit_card_utilization_delta_60d.increased',
    'entity_attribute.revolving_credit_card_utilization_delta_60d.decreased',
    'entity_attribute.revolving_credit_card_utilization_delta_90d.increased',
    'entity_attribute.revolving_credit_card_utilization_delta_90d.decreased',
    'entity_attribute.personal_loan_utilization_trend_90d.increased',
    'entity_attribute.personal_loan_utilization_trend_90d.decreased',
    'entity_attribute.personal_loan_utilization_delta_30d.increased',
    'entity_attribute.personal_loan_utilization_delta_30d.decreased',
    'entity_attribute.personal_loan_utilization_delta_60d.increased',
    'entity_attribute.personal_loan_utilization_delta_60d.decreased',
    'entity_attribute.personal_loan_utilization_delta_90d.increased',
    'entity_attribute.personal_loan_utilization_delta_90d.decreased',
    'entity_attribute.mortgage_balance_total.increased',
    'entity_attribute.mortgage_balance_total.decreased',
    'entity_attribute.mortgage_balance_change_30d.increased',
    'entity_attribute.mortgage_balance_change_30d.decreased',
    'entity_attribute.mortgage_balance_change_60d.increased',
    'entity_attribute.mortgage_balance_change_60d.decreased',
    'entity_attribute.mortgage_balance_change_90d.increased',
    'entity_attribute.mortgage_balance_change_90d.decreased',
    'entity_attribute.weighted_average_apr_mortgage.increased',
    'entity_attribute.weighted_average_apr_mortgage.decreased',
    'entity_attribute.mortgage_utilization_trend_30d.increased',
    'entity_attribute.mortgage_utilization_trend_30d.decreased',
    'entity_attribute.mortgage_utilization_trend_90d.increased',
    'entity_attribute.mortgage_utilization_trend_90d.decreased',
    'entity_attribute.mortgage_utilization_delta_30d.increased',
    'entity_attribute.mortgage_utilization_delta_30d.decreased',
    'entity_attribute.mortgage_utilization_delta_60d.increased',
    'entity_attribute.mortgage_utilization_delta_60d.decreased',
    'entity_attribute.mortgage_utilization_delta_90d.increased',
    'entity_attribute.mortgage_utilization_delta_90d.decreased',
    'entity_attribute.installment_balance_total.increased',
    'entity_attribute.installment_balance_total.decreased',
    'entity_attribute.installment_balance_change_30d.increased',
    'entity_attribute.installment_balance_change_30d.decreased',
    'entity_attribute.installment_balance_change_60d.increased',
    'entity_attribute.installment_balance_change_60d.decreased',
    'entity_attribute.installment_balance_change_90d.increased',
    'entity_attribute.installment_balance_change_90d.decreased',
    'entity_attribute.overall_utilization_trend_30d.increased',
    'entity_attribute.overall_utilization_trend_30d.decreased',
    'entity_attribute.overall_utilization_trend_90d.increased',
    'entity_attribute.overall_utilization_trend_90d.decreased',
    'entity_attribute.overall_utilization_delta_30d.increased',
    'entity_attribute.overall_utilization_delta_30d.decreased',
    'entity_attribute.overall_utilization_delta_60d.increased',
    'entity_attribute.overall_utilization_delta_60d.decreased',
    'entity_attribute.overall_utilization_delta_90d.increased',
    'entity_attribute.overall_utilization_delta_90d.decreased',
    'entity_attribute.other_balance_total.increased',
    'entity_attribute.other_balance_total.decreased',
    'entity_attribute.other_balance_change_30d.increased',
    'entity_attribute.other_balance_change_30d.decreased',
    'entity_attribute.other_balance_change_60d.increased',
    'entity_attribute.other_balance_change_60d.decreased',
    'entity_attribute.other_balance_change_90d.increased',
    'entity_attribute.other_balance_change_90d.decreased',
    'manual_connect.create',
    'manual_connect.update',
    'payment_instrument.create',
    'payment_instrument.update',
    'method_jwk.create',
    'method_jwk.update',
    'credit_score.available',
    'account.number.update',
    'account.balance_increased',
    'account.balance_decreased',
    'account.credit_limit_increased',
    'account.credit_limit_decreased',
    'entity.new_accounts_pending_consent',
    'entity_vehicle.create',
    'entity_vehicle.update',
    'attribute.credit_health_credit_card_usage.increased',
    'attribute.credit_health_credit_card_usage.decreased',
    'attribute.credit_health_derogatory_marks.increased',
    'attribute.credit_health_derogatory_marks.decreased',
    'attribute.credit_health_hard_inquiries.increased',
    'attribute.credit_health_hard_inquiries.decreased',
    'attribute.credit_health_total_accounts.increased',
    'attribute.credit_health_total_accounts.decreased',
    'attribute.credit_health_credit_age.increased',
    'attribute.credit_health_credit_age.decreased',
    'attribute.credit_health_payment_history.increased',
    'attribute.credit_health_payment_history.decreased',
    'attribute.credit_health_open_accounts.increased',
    'attribute.credit_health_open_accounts.decreased',
]


WebhookStatusesLiterals = Literal[
    'active',
    'disabled',
    'deleted',
    'requires_attention'
]


class Webhook(TypedDict):
    id: str
    type: WebhookTypesLiterals
    url: str
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str
    expand_event: bool
    status: Optional[WebhookStatusesLiterals]
    error: Optional[object]


class WebhookCreateOpts(TypedDict):
    type: WebhookTypesLiterals
    url: str
    auth_token: Optional[str]
    hmac_secret: Optional[str]
    metadata: Optional[Dict[str, Any]]
    expand_event: Optional[bool]


class WebhookUpdateOpts(TypedDict):
    status: Literal['active', 'disabled']


class WebhookResource(Resource):
    def __init__(self, config: Configuration):
        super(WebhookResource, self).__init__(config.add_path('webhooks'))

    def retrieve(self, _id: str) -> MethodResponse[Webhook]:
        return super(WebhookResource, self)._get_with_id(_id)

    def delete(self, _id: str) -> MethodResponse[Webhook]:
        res = super(WebhookResource, self)._delete(_id)
        return res

    def list(self) -> MethodResponse[List[Webhook]]:
        return super(WebhookResource, self)._list(None)

    def create(self, opts: WebhookCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[Webhook]:
        return super(WebhookResource, self)._create(opts, request_opts)

    def update(self, _id: str, opts: WebhookUpdateOpts) -> MethodResponse[Webhook]:
        return super(WebhookResource, self)._patch_with_id(_id, opts)
