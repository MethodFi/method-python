from typing import TypedDict, Optional, Dict, List, Any, Literal

from method.resource import Resource, RequestOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Verification import VerificationResource


AccountTypesLiterals = Literal[
    'ach',
    'liability',
    'clearing'
]


AccountSubTypes = Literal[
    'checking',
    'savings'
]


AccountCapabilitiesLiterals = Literal[
    'payments:receive',
    'payments:send'
]


AccountStatusesLiterals = Literal[
    'active',
    'disabled'
]


class AccountACH(TypedDict):
    routing: int
    number: int
    type: AccountSubTypes


class AccountLiability(TypedDict):
    mch_id: str
    mask: str


class AccountClearing(TypedDict):
    routing: int
    number: int


class AccountLiabilityCreateOpts(TypedDict):
    mch_id: str
    account_number: str


class Account(TypedDict):
    id: str
    holder_id: str
    status: AccountStatusesLiterals
    type: AccountTypesLiterals
    ach: Optional[AccountACH]
    liability: Optional[AccountLiability]
    clearing: Optional[AccountClearing]
    capabilities: List[AccountCapabilitiesLiterals]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str
    metadata: Optional[Dict[str, Any]]


class AccountCreateOpts(TypedDict):
    holder_id: str
    ach: Optional[AccountACH]
    liability: Optional[AccountLiabilityCreateOpts]
    metadata: Optional[Dict[str, Any]]


class AccountListOpts(TypedDict):
    holder_id: Optional[str]


class AccountSubResources:
    verification: VerificationResource

    def __init__(self, _id: str, config: Configuration):
        self.verification = VerificationResource(config.add_path(_id))


class AccountResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountResource, self).__init__(config.add_path('accounts'))

    def __call__(self, _id: str) -> AccountSubResources:
        return AccountSubResources(_id, self.config)

    def get(self, _id: str) -> Account:
        return super(AccountResource, self)._get_with_id(_id)

    def list(self, params: Optional[AccountListOpts] = None) -> List[Account]:
        return super(AccountResource, self)._list(params)

    def create(self, opts: AccountCreateOpts, request_opts: Optional[RequestOpts] = None) -> Account:
        return super(AccountResource, self)._create(opts, request_opts)
