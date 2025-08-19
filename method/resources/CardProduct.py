from typing import TypedDict, Optional, List, Literal

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.errors import ResourceError


CardProductTypeLiterals = Literal[
  'specific',
  'generic',
  'in_review',
]

class CardProductBrand(TypedDict):
  id: str
  description: str
  network: str
  default_image: str


class CardProduct(TypedDict):
  id: str
  name: str
  issuer: str
  type: CardProductTypeLiterals
  brands: List[CardProductBrand]
  error: Optional[ResourceError]
  created_at: str
  updated_at: str


class CardProductResource(Resource):
  def __init__(self, config: Configuration):
    super(CardProductResource, self).__init__(config.add_path('card_product'))


  def retrieve(self, prt_id: str) -> MethodResponse[CardProduct]:
    return super(CardProductResource, self)._get_with_id(prt_id)

