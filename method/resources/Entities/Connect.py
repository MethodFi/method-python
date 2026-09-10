from typing import TypedDict, Optional, Literal, List, Dict, Any, Union

from method.resource import MethodResponse, RequestOpts, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Accounts.Account import Account


EntityConnectResponseStatusLiterals = Literal[
    "completed", "in_progress", "pending", "failed"
]

EntityConnectArtifactTypesLiterals = Literal[
    'raw_credit_report',
    'credit_report_pdf'
]

EntityConnectFileBureausLiterals = Literal[
    'equifax',
    'transunion'
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


class EntityConnectFile(TypedDict):
    id: str
    type: EntityConnectArtifactTypesLiterals
    bureau: EntityConnectFileBureausLiterals
    mime_type: str


class EntityConnect(TypedDict):
    id: str
    entity_id: str
    status: EntityConnectResponseStatusLiterals
    accounts: Optional[List[Union[str, Account]]]
    requested_products: List[AccountProductsEligibleForAutomaticExecutionLiteral]
    requested_subscriptions: List[AccountSubscriptionsEligibleForAutomaticExecutionLiteral]
    files: List[EntityConnectFile]
    credit_reports: Optional[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class ConnectExpandOpts(TypedDict):
    expand: List[AccountConnectResponseExpandLiterals]


class ConnectResourceListOpts(ResourceListOpts, ConnectExpandOpts):
    pass

class ConnectCreateOpts(TypedDict):
    products: Optional[List[AccountProductsEligibleForAutomaticExecutionLiteral]]
    subscriptions: Optional[List[AccountSubscriptionsEligibleForAutomaticExecutionLiteral]]
    artifacts: Optional[List[EntityConnectArtifactTypesLiterals]]
    bureau: Optional[EntityConnectFileBureausLiterals]




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
        params: Optional[ConnectExpandOpts] = None,
        request_opts: Optional[RequestOpts] = None
    ) -> MethodResponse[EntityConnect]:
        return super(EntityConnectResource, self)._create(data=opts, params=params, request_opts=request_opts)
 