from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource
from method.configuration import Configuration


AccountSubscriptionTypesLiterals = Literal[
    'transaction',
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
    'transaction': Optional[AccountSubscription],
    'update': Optional[AccountSubscription],
    'update.snapshot': Optional[AccountSubscription]
})


class AccountSubscriptionCreateOpts(TypedDict):
    enroll: AccountSubscriptionTypesLiterals


class AccountSubscriptionsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountSubscriptionsResource, self).__init__(config.add_path('subscriptions'))

    def create(self, sub_name: AccountSubscriptionCreateOpts) -> MethodResponse[AccountSubscription]:
        return super(AccountSubscriptionsResource, self)._create({ 'enroll': sub_name })
    
    def list(self) -> MethodResponse[List[AccountSubscription]]:
        return super(AccountSubscriptionsResource, self)._get()
    
    def retrieve(self, sub_id: str) -> MethodResponse[AccountSubscriptionsResponse]:
        return super(AccountSubscriptionsResource, self)._get_with_id(sub_id)
    
    def delete(self, sub_id: str) -> MethodResponse[AccountSubscription]:
        return super(AccountSubscriptionsResource, self)._delete(sub_id)
   