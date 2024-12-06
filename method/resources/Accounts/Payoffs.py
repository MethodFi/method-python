from typing import List, TypedDict, Optional, Literal

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError


AccountPayoffStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


class AccountPayoff(TypedDict):
    id: str
    account_id: str
    status: AccountPayoffStatusesLiterals
    amount: Optional[int]
    term: Optional[int]
    per_diem_amount: Optional[int]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountPayoffsResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountPayoffsResource, self).__init__(config.add_path('payoffs'))

    def retrieve(self, pyf_id: str) -> MethodResponse[AccountPayoff]:
        return super(AccountPayoffsResource, self)._get_with_id(pyf_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountPayoff]]:
        return super(AccountPayoffsResource, self)._list(params)
    
    def create(self) -> MethodResponse[AccountPayoff]:
        return super(AccountPayoffsResource, self)._create({})
