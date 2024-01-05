from typing import TypedDict, Optional

from method.resource import Resource, RequestOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Verification import VerificationResource


class AccountSync(TypedDict):
    id: str
    acc_id: str
    status: str
    error: Optional[ResourceError]
    created_at: str
    updated_at: str

class AccountSyncCreateOpts(TypedDict):
    pass

class AccountSyncResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountSyncResource, self).__init__(config.add_path('syncs'))

    def get(self, _id: str) -> AccountSync:
        return super(AccountSyncResource, self)._get_with_id(_id)

    def create(self, opts: Optional[AccountSyncCreateOpts] = {}) -> AccountSync:
        return super(AccountSyncResource, self)._create(opts)
