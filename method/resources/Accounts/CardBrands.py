from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


class AccountCardBrandInfo(TypedDict):
    art_id: str
    url: str
    name: str


class AccountCardBrand(TypedDict):
    id: str
    account_id: str
    network: str
    issuer: str
    last4: str
    brands: List[AccountCardBrandInfo]
    status: Literal['completed', 'failed']
    shared: bool
    source: Optional[Literal['method', 'network']]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountCardBrandsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountCardBrandsResource, self).__init__(config.add_path('card_brands'))

    def retrieve(self, crbd_id: str) -> MethodResponse[AccountCardBrand]:
        return super(AccountCardBrandsResource, self)._get_with_id(crbd_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountCardBrand]]:
        return super(AccountCardBrandsResource, self)._list(params)
    
    def create(self) -> MethodResponse[AccountCardBrand]:
        return super(AccountCardBrandsResource, self)._create({})
