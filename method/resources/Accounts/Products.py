from typing import TypedDict, Optional, Literal

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.errors import ResourceError


AccountProductTypeStatusLiterals = Literal[
    'unavailable',
    'available',
    'restricted'
]


class AccountProduct(TypedDict):
    id: str
    name: str
    status: AccountProductTypeStatusLiterals
    status_error: Optional[ResourceError]
    latest_request_id: str
    is_subscribable: bool
    created_at: str
    updated_at: str


class AccountProductListResponse(TypedDict):
    attribute: Optional[AccountProduct]
    balance: Optional[AccountProduct]
    payment: Optional[AccountProduct]
    sensitive: Optional[AccountProduct]
    update: Optional[AccountProduct]
    transactions: Optional[AccountProduct]
    payoff: Optional[AccountProduct]
    card_brand: Optional[AccountProduct]
    payment_instruments: Optional[AccountProduct]

class AccountProductResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountProductResource, self).__init__(config.add_path('products'))

    def retrieve(self, prd_id: str) -> MethodResponse[AccountProduct]:
        return super(AccountProductResource, self)._get_with_id(prd_id)

    def list(self) -> MethodResponse[AccountProductListResponse]:
        return super(AccountProductResource, self)._list()
