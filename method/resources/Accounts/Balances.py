from typing import List, TypedDict, Optional, Literal

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError

AccountBalanceStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


class AccountBalance(TypedDict):
    id: str
    account_id: str
    status: AccountBalanceStatusLiterals
    amount: Optional[int]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str
    

class AccountBalancesResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountBalancesResource, self).__init__(config.add_path('balances'))

    def retrieve(self, bal_id: str) -> MethodResponse[AccountBalance]:
        return super(AccountBalancesResource, self)._get_with_id(bal_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountBalance]]:
        return super(AccountBalancesResource, self)._list(params)

    def create(self) -> MethodResponse[AccountBalance]:
        return super(AccountBalancesResource, self)._create({})
