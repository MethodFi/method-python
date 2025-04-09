from typing import TypedDict, Optional, List, Literal, Union

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Accounts.ExternalTypes import PlaidBalance, PlaidTransaction, MXAccount, MXTransaction, TellerBalance, TellerTransaction


AccountVerificationSessionStatusesLiterals = Literal[
    'pending',
    'in_progress',
    'verified',
    'failed'
]


AccountVerificationSessionTypesLiterals = Literal[
    'micro_deposits',
    'plaid',
    'mx',
    'teller',
    'standard',
    'instant',
    'pre_auth',
    'network'
]


AccountVerificationPassFailLiterals = Literal[
    'pass',
    'fail'
]


class AccountVerificationSessionMicroDeposits(TypedDict):
    amounts: List[int]


class AccountVerificationSessionPlaid(TypedDict):
    balances: PlaidBalance
    transactions: List[PlaidTransaction]


class AccountVerificationSessionMX(TypedDict):
    accounts: MXAccount
    transactions: List[MXTransaction]


class AccountVerificationSessionTeller(TypedDict):
    balances: TellerBalance
    transactions: List[TellerTransaction]


class AccountVerificationSessionTrustProvisioner(TypedDict):
    pass


class AccountVerificationSessionAutoVerify(TypedDict):
    pass


class AccountVerificationSessionThreeDS(TypedDict):
    pass


class AccountVerificationSessionIssuer(TypedDict):
    pass


class AccountVerificationSessionStandard(TypedDict):
    number: str


class AccountVerificationSessionInstant(TypedDict):
    exp_year: Optional[str]
    exp_month: Optional[str]
    exp_check: Optional[AccountVerificationPassFailLiterals]
    number: Optional[str]


class AccountVerificationSessionPreAuth(AccountVerificationSessionInstant):
    cvv: str
    cvv_check: Optional[AccountVerificationPassFailLiterals]
    billing_zip_code: str
    billing_zip_code_check: Optional[AccountVerificationPassFailLiterals]
    pre_auth_check: Optional[AccountVerificationPassFailLiterals]


class AccountVerificationSessionNetwork(AccountVerificationSessionInstant):
    cvv: str
    cvv_check: Optional[AccountVerificationPassFailLiterals]
    billing_zip_code: str
    billing_zip_code_check: Optional[AccountVerificationPassFailLiterals]
    network_check: Optional[AccountVerificationPassFailLiterals]

class AccountVerificationSessionCreateOpts(TypedDict):
    type: AccountVerificationSessionTypesLiterals


class AccountVerificationSessionMicroDepositsUpdateOpts(TypedDict):
    micro_deposits: AccountVerificationSessionMicroDeposits


class AccountVerificationSessionPlaidUpdateOpts(TypedDict):
    plaid: AccountVerificationSessionPlaid


class AccountVerificationSessionMXUpdateOpts(TypedDict):
    mx: AccountVerificationSessionMX


class AccountVerificationSessionTellerUpdateOpts(TypedDict):
    teller: AccountVerificationSessionTeller


class AccountVerificationSessionStandardUpdateOpts(TypedDict):
    standard: AccountVerificationSessionStandard


class AccountVerificationSessionInstantUpdateOpts(TypedDict):
    instant: AccountVerificationSessionInstant


class AccountVerificationSessionPreAuthUpdateOpts(TypedDict):
    pre_auth: AccountVerificationSessionPreAuth


class AccountVerificationSessionNetworkUpdateOpts(TypedDict):
    network: AccountVerificationSessionNetwork


AccountVerificationSessionUpdateOpts = Union[
    AccountVerificationSessionMicroDepositsUpdateOpts,
    AccountVerificationSessionPlaidUpdateOpts,
    AccountVerificationSessionMXUpdateOpts,
    AccountVerificationSessionTellerUpdateOpts,
    AccountVerificationSessionStandardUpdateOpts,
    AccountVerificationSessionInstantUpdateOpts,
    AccountVerificationSessionPreAuthUpdateOpts,
    AccountVerificationSessionNetworkUpdateOpts
]


class AccountVerificationSession(TypedDict):
    id: str
    status: AccountVerificationSessionStatusesLiterals
    type: AccountVerificationSessionTypesLiterals
    error: Optional[ResourceError]
    plaid: Optional[AccountVerificationSessionPlaid]
    mx: Optional[AccountVerificationSessionMX]
    teller: Optional[AccountVerificationSessionTeller]
    micro_deposits: Optional[AccountVerificationSessionMicroDeposits]
    trust_provisioner: Optional[AccountVerificationSessionTrustProvisioner]
    auto_verify: Optional[AccountVerificationSessionAutoVerify]
    standard: Optional[AccountVerificationSessionStandard]
    instant: Optional[AccountVerificationSessionInstant]
    pre_auth: Optional[AccountVerificationSessionPreAuth]
    three_ds: Optional[AccountVerificationSessionThreeDS]
    issuer: Optional[AccountVerificationSessionIssuer]
    network: Optional[AccountVerificationSessionNetwork]
    created_at: str
    updated_at: str

  
class AccountVerificationSessionResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountVerificationSessionResource, self).__init__(config.add_path('verification_sessions'))

    def create(self, opts: AccountVerificationSessionCreateOpts) -> MethodResponse[AccountVerificationSession]:
        return super(AccountVerificationSessionResource, self)._create(opts)

    def retrieve(self, avs_id: str) -> MethodResponse[AccountVerificationSession]:
        return super(AccountVerificationSessionResource, self)._get_with_id(avs_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountVerificationSession]]:
        return super(AccountVerificationSessionResource, self)._list(params)

    def update(self, avs_id: str, opts: AccountVerificationSessionUpdateOpts) -> MethodResponse[AccountVerificationSession]:
        return super(AccountVerificationSessionResource, self)._update_with_id(avs_id, opts)
