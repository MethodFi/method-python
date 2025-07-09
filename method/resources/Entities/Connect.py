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
    "attribute",
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

class ConnectCreateOpts(TypedDict):
    products: Optional[List[AccountProductsEligibleForAutomaticExecutionLiteral]]
    subscriptions: Optional[List[AccountSubscriptionsEligibleForAutomaticExecutionLiteral]]




class EntityConnectResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityConnectResource, self).__init__(config.add_path("connect"))

    def retrieve(self, cxn_id: str, opts: Optional[ConnectExpandOpts] = None) -> MethodResponse[EntityConnect]:
        return super(EntityConnectResource, self)._get_with_sub_path_and_params(cxn_id, params=opts)

    def list(
        self, opts: Optional[ConnectResourceListOpts] = None
    ) -> MethodResponse[List[EntityConnect]]:
        return super(EntityConnectResource, self)._list(opts)
    
    def create(
        self,
        opts: ConnectCreateOpts = {},
        params: Optional[ConnectExpandOpts] = None
    ) -> MethodResponse[EntityConnect]:
        return super(EntityConnectResource, self)._create(data=opts, params=params)
 