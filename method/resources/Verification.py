from typing import TypedDict, List, Literal, Dict, Any, Optional

from method.resource import Resource
from method.configuration import Configuration
from method.errors import ResourceError


VerificationStatusesLiterals = Literal[
    'initiated',
    'pending',
    'verified',
    'disabled'
]


VerificationTypesLiterals = Literal[
    'micro_deposits',
    'plaid',
    'mx',
    'auto_verify',
    'trusted_provisioner'
]


class Verification(TypedDict):
    id: str
    status: VerificationStatusesLiterals
    type: VerificationTypesLiterals
    error: Optional[ResourceError]
    initiated_at: str
    pending_at: str
    verified_at: str
    disabled_at: str
    created_at: str
    updated_at: str


class VerificationMicroDepositsUpdate(TypedDict):
    amounts: List[int]


class VerificationUpdateOpts(TypedDict):
    micro_deposits: VerificationMicroDepositsUpdate


class VerificationPlaidCreate(TypedDict):
    balances: Dict[str, Any]
    transactions: List[Dict[str, Any]]


class VerificationMXCreate(TypedDict):
    account: Dict[str, Any]
    transactions: List[Dict[str, Any]]


class VerificationCreateOpts(TypedDict):
    type: VerificationTypesLiterals
    plaid: Optional[VerificationPlaidCreate]
    mx: Optional[VerificationMXCreate]


class VerificationTestAmountsResponse(TypedDict):
    amounts: List[int]


class VerificationResource(Resource):
    def __init__(self, config: Configuration):
        super(VerificationResource, self).__init__(config.add_path('verification'))

    def get(self) -> Verification:
        return super(VerificationResource, self)._get()

    def update(self, opts: VerificationUpdateOpts) -> Verification:
        return super(VerificationResource, self)._update(opts)

    def create(self, opts: VerificationCreateOpts) -> Verification:
        return super(VerificationResource, self)._create(opts)

    def get_test_amounts(self) -> VerificationTestAmountsResponse:
        return super(VerificationResource, self)._get_with_sub_path('amounts')
