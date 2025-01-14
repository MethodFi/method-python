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
    'balance.create',
    'balance.update',
    'identity.create',
    'identity.update',
    'account_verification_session.create',
    'account_verification_session.update',
    'card_brand.create',
    'card_brand.update',
    'sensitive.create',
    'sensitive.update',
    'update.create',
    'update.update',
    'attribute.create',
    'attribute.update',
    'account.opened',
    'account.closed',
    'credit_score.increased',
    'credit_score.decreased',
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


class Webhook(TypedDict):
    id: str
    type: WebhookTypesLiterals
    url: str
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str
    expand_event: bool
    status: str
    error: Optional[object]


class WebhookCreateOpts(TypedDict):
    type: WebhookTypesLiterals
    url: str
    auth_token: Optional[str]
    metadata: Optional[Dict[str, Any]]
    expand_event: Optional[bool]


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
