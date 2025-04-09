from typing import TypedDict, Optional, Literal, List, Any

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError

AccountPaymentInstrumentTypesLiterals = Literal[
    'card',
    'network_token'
]

class AccountPaymentInstrumentCreateOpts(TypedDict):
    type: AccountPaymentInstrumentTypesLiterals

class AccountPaymentInstrumentNetworkToken(TypedDict):
    token: str

class AccountPaymentInstrumentCard(TypedDict):
    number: str
    exp_month: int
    exp_year: int

AccountPaymentInstrumentStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]

class AccountPaymentInstrument(TypedDict):
    id: str
    account_id: str
    type: AccountPaymentInstrumentTypesLiterals
    network_token: Optional[AccountPaymentInstrumentNetworkToken]
    card: Optional[AccountPaymentInstrumentCard]
    chargeable: bool
    status: AccountPaymentInstrumentStatusesLiterals
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountPaymentInstrumentsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountPaymentInstrumentsResource, self).__init__(config.add_path('payment_instruments'))

    def retrieve(self, pmt_inst_id: str) -> MethodResponse[AccountPaymentInstrument]:
        return super(AccountPaymentInstrumentsResource, self)._get_with_id(pmt_inst_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountPaymentInstrument]]:
        return super(AccountPaymentInstrumentsResource, self)._list(params)

    def create(self, data: AccountPaymentInstrumentCreateOpts) -> MethodResponse[AccountPaymentInstrument]:
        return super(AccountPaymentInstrumentsResource, self)._create(data)
