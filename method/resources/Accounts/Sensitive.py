from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


AccountSensitiveFieldsLiterals = Literal[
    'auto_loan.number',
    'mortgage.number',
    'personal_loan.number',
    'credit_card.number',
    'credit_card.billing_zip_code',
    'credit_card.exp_month',
    'credit_card.exp_year',
    'credit_card.cvv'
]


class AccountSensitiveLoan(TypedDict):
    number: str


class AccountSensitiveCreditCard(TypedDict):
    number: Optional[str]
    billing_zip_code: Optional[str]
    exp_month: Optional[str]
    exp_year: Optional[str]
    cvv: Optional[str]


class AccountSensitive(TypedDict):
    id: str
    account_id: str
    auto_loan: Optional[AccountSensitiveLoan]
    credit_card: Optional[AccountSensitiveCreditCard]
    mortgage: Optional[AccountSensitiveLoan]
    personal_loan: Optional[AccountSensitiveLoan]
    status: Literal['completed', 'failed']
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountSensitiveCreateOpts(TypedDict):
    expand: List[AccountSensitiveFieldsLiterals]


class AccountSensitiveResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountSensitiveResource, self).__init__(config.add_path('sensitive'))

    def retrieve(self, astv_id: str) -> MethodResponse[AccountSensitive]:
        return super(AccountSensitiveResource, self)._get_with_id(astv_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountSensitive]]:
        return super(AccountSensitiveResource, self)._list(params)

    def create(self, data: AccountSensitiveCreateOpts) -> MethodResponse[AccountSensitive]:
        return super(AccountSensitiveResource, self)._create(data)
