from typing import TypedDict, Optional, Literal, List

from method.resource import Resource
from method.configuration import Configuration
from method.errors import ResourceError


AccountBalanceSensitiveFeildsLiterals = Literal[
    'number',
    'billing_zip_code',
    'exp_month',
    'exp_year',
    'cvv',
]


class AccountSensitive(TypedDict):
    id: str
    account_id: str
    number: Optional[str]
    exp_month: Optional[str]
    exp_year: Optional[str]
    cvv: Optional[str]
    billing_zip_code: Optional[str]
    status: Literal['completed', 'failed']
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountSensitiveCreateOpts(TypedDict):
    expand: List[AccountBalanceSensitiveFeildsLiterals]


class AccountSensitiveResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountSensitiveResource, self).__init__(config.add_path('sensitive'))

    def retrieve(self, astv_id: str) -> AccountSensitive:
        return super(AccountSensitiveResource, self)._get_with_id(astv_id)

    def create(self, data: AccountSensitiveCreateOpts) -> AccountSensitive:
        return super(AccountSensitiveResource, self)._create(data)