from typing import TypedDict, Optional, List, Literal

from method.resource import Resource
from method.configuration import Configuration
from method.errors import ResourceError


EntitySubscriptionNamesLiterals = Literal[
    'connect',
    'credit_score'
]


EntitySubscriptionStatusesLiterals = Literal[
    'active',
    'inactive'
]


class EntitySubscription(TypedDict):
    id: str
    name: EntitySubscriptionNamesLiterals
    status: EntitySubscriptionStatusesLiterals
    last_request_id: Optional[str]
    created_at: str
    updated_at: str


class EntitySubscriptionResponseOpts(TypedDict):
    subscription: Optional[EntitySubscription]
    error: Optional[ResourceError]


class EntitySubscriptionCreateOpts(TypedDict):
    enroll: List[EntitySubscriptionNamesLiterals]


class EntitySubscriptionListResponse(TypedDict):
    connect: Optional[EntitySubscriptionResponseOpts]
    credit_score: Optional[EntitySubscriptionResponseOpts]


class EntitySubscriptionsResource(Resource):
    def __init__(self, config: Configuration):
        super(EntitySubscriptionsResource, self).__init__(config.add_path('subscriptions'))

    def retrieve(self, sub_id: str) -> EntitySubscriptionResponseOpts:
        return super(EntitySubscriptionsResource, self)._get_with_id(sub_id)

    def list(self) -> EntitySubscriptionListResponse:
        return super(EntitySubscriptionsResource, self)._list()

    def create(self, opts: EntitySubscriptionCreateOpts) -> EntitySubscriptionResponseOpts:
        return super(EntitySubscriptionsResource, self)._create(opts)
    
    def delete(self, sub_id: str) -> EntitySubscriptionResponseOpts:
        return super(EntitySubscriptionsResource, self)._delete(sub_id)