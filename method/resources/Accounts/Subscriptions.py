from typing import TypedDict, Optional, Literal, List

from method.resource import Resource
from method.configuration import Configuration


AccountSubscriptionTypesLiterals = Literal[
    'transactions',
    'update',
    'update.snapshot'
]


class AccountSubscription(TypedDict):
    id: str
    name: AccountSubscriptionTypesLiterals
    status: Literal['active']
    latest_transaction_id: str
    created_at: str
    updated_at: str


AccountSubscriptionsResponse = TypedDict('AccountSubscriptionsResponse', {
    'transactions': Optional[AccountSubscription],
    'update': Optional[AccountSubscription],
    'update.snapshot': Optional[AccountSubscription]
})


class AccountSubscriptionCreateOpts(TypedDict):
    enroll: List[AccountSubscriptionTypesLiterals]


class AccountSubscriptionsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountSubscriptionsResource, self).__init__(config.add_path('subscriptions'))

    def create(self, data: AccountSubscriptionCreateOpts) -> AccountSubscription:
        return super(AccountSubscriptionsResource, self)._create(data)
    
    def list(self) -> List[AccountSubscription]:
        return super(AccountSubscriptionsResource, self)._get()
    
    def retrieve(self, sub_id: str) -> AccountSubscriptionsResponse:
        return super(AccountSubscriptionsResource, self)._get_with_id(sub_id)
    
    def delete(self, sub_id: str) -> AccountSubscription:
        return super(AccountSubscriptionsResource, self)._delete(sub_id)
    