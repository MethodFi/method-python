from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


class AccountCardBrandRewardCategory(TypedDict):
    category: Optional[str]
    category_presentable: Optional[str]
    rate: Optional[float]
    unit: Optional[str]
    cap: Optional[str]


class AccountCardBrandRewards(TypedDict):
    type: Optional[str]
    program: Optional[str]
    categories: List[AccountCardBrandRewardCategory]


class AccountCardBrandQualifyingPeriod(TypedDict):
    value: int
    unit: str
    relative_to: str


class AccountCardBrandPromotion(TypedDict):
    type: Optional[str]
    title: Optional[str]
    description: Optional[str]
    value: Optional[float]
    unit: Optional[str]
    spend_requirement: Optional[int]
    qualifying_period: Optional[AccountCardBrandQualifyingPeriod]
    expiration: Optional[str]


class AccountCardBrandDetails(TypedDict):
    card_category: Optional[str]
    purchase_apr_min: Optional[float]
    purchase_apr_max: Optional[float]
    cash_advance_apr_min: Optional[float]
    cash_advance_apr_max: Optional[float]
    annual_fee: Optional[int]
    late_payment_fee: Optional[int]
    rewards: AccountCardBrandRewards
    promotions: List[AccountCardBrandPromotion]
    data_as_of: Optional[str]


class AccountCardBrandInfo(TypedDict):
  id: str
  card_product_id: str
  description: str
  name: str
  issuer: str
  network: str
  network_tier: Optional[str]
  type: Literal['specific', 'generic', 'in_review']
  url: str
  details: Optional[AccountCardBrandDetails]


class AccountCardBrand(TypedDict):
    id: str
    account_id: str
    brands: List[AccountCardBrandInfo]
    status: Literal['completed', 'pending', 'in_progress', 'failed']
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
