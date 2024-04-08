from typing import TypedDict, Optional, Literal

from method.resource import Resource
from method.configuration import Configuration
from method.errors import ResourceError


EntitySyncTypeLiterals = Literal[
    'capabilities',
    'accounts'
]


class EntitySync(TypedDict):
    id: str
    acc_id: str
    status: str
    type: str
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntitySyncCreateOpts(TypedDict):
    type: EntitySyncTypeLiterals


class EntitySyncResource(Resource):
    def __init__(self, config: Configuration):
        super(EntitySyncResource, self).__init__(config.add_path('syncs'))

    def retrieve(self, acc_sync_id: str) -> EntitySync:
        return super(EntitySyncResource, self)._get_with_id(acc_sync_id)

    def create(self, opts: Optional[EntitySyncCreateOpts] = {}) -> EntitySync:
        return super(EntitySyncResource, self)._create(opts)
