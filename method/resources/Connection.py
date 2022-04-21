from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resources import Account
from method.errors import ResourceError
from method.resource import Resource
from method.configuration import Configuration


ConnectionSourcesLiterals = Literal[
    'plaid',
    'mch_5500'
]


ConnectionStatusesLiterals = Literal[
    'success',
    'reauth_required',
    'syncing',
    'failed'
]


class Connection(TypedDict):
    id: str
    entity_id: str
    accounts: List[str]
    source: ConnectionSourcesLiterals
    status: ConnectionStatusesLiterals
    error: Optional[ResourceError]
    created_at: str
    updated_at: str
    last_synced_at: str


class ConnectionUpdateOpts(TypedDict):
    status: Literal['syncing']


class ConnectionResource(Resource):
    def __init__(self, config: Configuration):
        super(ConnectionResource, self).__init__(config.add_path('connections'))

    def get(self, _id: str) -> Connection:
        return super(ConnectionResource, self)._get_with_id(_id)

    def list(self) -> List[Connection]:
        return super(ConnectionResource, self)._list(None)

    def update(self, _id: str, opts: ConnectionUpdateOpts) -> Connection:
        return super(ConnectionResource, self)._update_with_id(_id, opts)

    def get_public_account_tokens(self, _id: str) -> List[str]:
        return super(ConnectionResource, self)._get_with_sub_path('{_id}/public_account_tokens'.format(_id=_id))
