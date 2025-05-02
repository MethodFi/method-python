from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


EntityAttributesResponseStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


CreditHealthAttributeRating = Literal[
    'excellent',
    'good',
    'fair',
    'needs_work'
]


class CreditHealthAttribute(TypedDict):
    value: int
    rating: CreditHealthAttributeRating


class EntityAttributesType(TypedDict):
    credit_health_credit_card_usage: CreditHealthAttribute
    credit_health_derogatory_marks: CreditHealthAttribute
    credit_health_hard_inquiries: CreditHealthAttribute
    credit_health_total_accounts: CreditHealthAttribute
    credit_health_credit_age: CreditHealthAttribute
    credit_health_payment_history: CreditHealthAttribute
    credit_health_open_accounts: CreditHealthAttribute

class EntityAttributesCreateOpts(TypedDict):
    attributes: List[EntityAttributesType]

class EntityAttributes(TypedDict):
    id: str
    entity_id: str
    status: EntityAttributesResponseStatusLiterals
    attributes: Optional[List[EntityAttributesType]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityAttributesResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityAttributesResource, self).__init__(config.add_path('attributes'))

    def retrieve(self, attr_id: str) -> MethodResponse[EntityAttributes]:
        return super(EntityAttributesResource, self)._get_with_id(attr_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[EntityAttributes]]:
        return super(EntityAttributesResource, self)._list(params)

    def create(self, opts: EntityAttributesCreateOpts) -> MethodResponse[EntityAttributes]:
        return super(EntityAttributesResource, self)._create(opts)
