from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resource import Resource, RequestOpts
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
    'account_verification.sent',
    'account_verification.returned'
]


class Webhook(TypedDict):
    id: str
    type: WebhookTypesLiterals
    url: str
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str


class WebhookCreateOpts(TypedDict):
    type: WebhookTypesLiterals
    url: str
    auth_token: Optional[str]
    metadata: Optional[Dict[str, Any]]


class WebhookResource(Resource):
    def __init__(self, config: Configuration):
        super(WebhookResource, self).__init__(config.add_path('webhooks'))

    def get(self, _id: str) -> Webhook:
        return super(WebhookResource, self)._get_with_id(_id)

    def delete(self, _id: str) -> Webhook:
        return super(WebhookResource, self)._delete(_id)

    def list(self) -> List[Webhook]:
        return super(WebhookResource, self)._list(None)

    def create(self, opts: WebhookCreateOpts, request_opts: Optional[RequestOpts] = None) -> Webhook:
        return super(WebhookResource, self)._create(opts, request_opts)
