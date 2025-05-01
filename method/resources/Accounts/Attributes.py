from typing import TypedDict, Optional, Literal, List, Any, Dict

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


class AccountAttribute(TypedDict):
    value: Any


class AccountAttributesType(TypedDict):
    usage_pattern: AccountAttribute
    account_standing: AccountAttribute
    delinquent_period: AccountAttribute
    delinquent_outcome: AccountAttribute
    delinquent_amount: AccountAttribute
    utilization: AccountAttribute

AccountAttributesStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]

class AccountAttributes(TypedDict):
    id: str
    account_id: str
    status: AccountAttributesStatusesLiterals
    payload: Optional[Dict[str, Any]]
    attributes: Optional[List[AccountAttributesType]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountAttributesResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountAttributesResource, self).__init__(config.add_path('attributes'))

    def retrieve(self, acc_attr_id: str) -> MethodResponse[AccountAttributes]:
        return super(AccountAttributesResource, self)._get_with_id(acc_attr_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountAttributes]]:
        return super(AccountAttributesResource, self)._list(params)

    def create(self) -> MethodResponse[AccountAttributes]:
        return super(AccountAttributesResource, self)._create({})
