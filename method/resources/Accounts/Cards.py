from typing import TypedDict, Optional, Literal, List

from method.resource import Resource
from method.configuration import Configuration
from method.errors import ResourceError


class AccountCardBrand(TypedDict):
    art_id: str
    url: str
    name: str


class AccountCard(TypedDict):
    id: str
    account_id: str
    network: str
    issuer: str
    last4: str
    brands: List[AccountCardBrand]
    status: Literal['completed', 'failed']
    shared: bool
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountCardsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountCardsResource, self).__init__(config.add_path('cards'))

    def retrieve(self, crd_id: str) -> AccountCard:
        return super(AccountCardsResource, self)._get_with_id(crd_id)
    
    def _create(self) -> AccountCard:
        return super(AccountCardsResource, self)._create({})