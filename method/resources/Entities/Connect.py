from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


EntityConnectResponseStatusLiterals = Literal[
    "completed", "in_progress", "pending", "failed"
]

AccountConnectResponseExpandLiterals = Literal[
    "accounts",
    "accounts.sensitive",
    "accounts.balance",
    "accounts.card_brand",
    "accounts.attribute",
    "accounts.payoff",
    "accounts.transaction",
    "accounts.update",
    "accounts.payment_instrument",
    "accounts.latest_verification_session",
]

AccountProductsEligibleForAutomaticExecutionLiteral = Literal[
    "account_attribute",
    "balance",
    "card_brand",
    "update",
    "payoff",
]


AccountSubscriptionsEligibleForAutomaticExecutionLiteral = Literal[
    "card_brand", "update", "update.snapshot", "transaction"
]


class EntityConnect(TypedDict):
    id: str
    status: EntityConnectResponseStatusLiterals
    accounts: Optional[List[str]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class ConnectExpandOpts(TypedDict):
    expand: AccountConnectResponseExpandLiterals


class ConnectResourceListOpts(ResourceListOpts, ConnectExpandOpts):
    pass

class EntityConnectResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityConnectResource, self).__init__(config.add_path("connect"))

    def retrieve(self, cxn_id: str, params: Optional[ConnectExpandOpts] = None) -> MethodResponse[EntityConnect]:
        return super(EntityConnectResource, self)._get_with_sub_path_and_params(cxn_id, params=params)

    def list(
        self, params: Optional[ConnectResourceListOpts] = None
    ) -> MethodResponse[List[EntityConnect]]:
        return super(EntityConnectResource, self)._list(params)

    def create(
        self,
        products: Optional[List[AccountProductsEligibleForAutomaticExecutionLiteral]] = None,
        subscriptions: Optional[List[AccountSubscriptionsEligibleForAutomaticExecutionLiteral]] = None,
        params: Optional[ConnectExpandOpts] = None
    ) -> MethodResponse[EntityConnect]:
        data = {}
        if products:
            data["products"] = products
        if subscriptions:
            data["subscriptions"] = subscriptions
        return super(EntityConnectResource, self)._create(data=data, params=params)
 