from typing import TypedDict, Optional, Literal, List, Union

from method.resource import MethodResponse, Resource
from method.configuration import Configuration


AccountSubscriptionTypesLiterals = Literal[
    'attribute',
    'card_brand',
    'payment_instrument',
    'payment_instrument.card',
    'payment_instrument.network_token',
    'transaction',
    'update',
    'update.snapshot'
]


class AccountSubscriptionPayloadAttributes(TypedDict):
    requested_attributes: Optional[List[str]]
    bundles: Optional[List[str]]


class AccountSubscriptionPayload(TypedDict):
    attributes: Optional[AccountSubscriptionPayloadAttributes]


class AccountSubscription(TypedDict):
    id: str
    name: AccountSubscriptionTypesLiterals
    status: Literal['active']
    payload: Optional[AccountSubscriptionPayload]
    latest_request_id: Optional[str]
    created_at: str
    updated_at: str


AccountSubscriptionsResponse = TypedDict('AccountSubscriptionsResponse', {
    'attribute': Optional[AccountSubscription],
    'card_brand': Optional[AccountSubscription],
    'payment_instrument': Optional[AccountSubscription],
    'payment_instrument.card': Optional[AccountSubscription],
    'payment_instrument.network_token': Optional[AccountSubscription],
    'transaction': Optional[AccountSubscription],
    'update': Optional[AccountSubscription],
    'update.snapshot': Optional[AccountSubscription]
})


class AccountSubscriptionCreateOpts(TypedDict):
    enroll: AccountSubscriptionTypesLiterals
    payload: Optional[AccountSubscriptionPayload]


class AccountSubscriptionsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountSubscriptionsResource, self).__init__(config.add_path('subscriptions'))

    def create(self, opts: Union[AccountSubscriptionCreateOpts, AccountSubscriptionTypesLiterals]) -> MethodResponse[AccountSubscription]:
        if isinstance(opts, str):
            opts = {'enroll': opts}
        return super(AccountSubscriptionsResource, self)._create(opts)
    
    def list(self) -> MethodResponse[AccountSubscriptionsResponse]:
        return super(AccountSubscriptionsResource, self)._get()

    def retrieve(self, sub_id: str) -> MethodResponse[AccountSubscription]:
        return super(AccountSubscriptionsResource, self)._get_with_id(sub_id)
    
    def delete(self, sub_id: str) -> MethodResponse[AccountSubscription]:
        return super(AccountSubscriptionsResource, self)._delete(sub_id)
   