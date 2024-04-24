from typing import TypedDict, Optional, Literal, List

from method.resource import Resource
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Entities.Entity import EntityIdentity


EntityVerificationSessionStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


class EntityIdentity(TypedDict):
    id: str
    status: EntityVerificationSessionStatusLiterals
    identities: List[EntityIdentity]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityIdentityResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityIdentityResource, self).__init__(config.add_path('identities'))

    def retrieve(self, identity_id: str) -> EntityIdentity:
        return super(EntityIdentityResource, self)._get_with_id(identity_id)

    def create(self, opts: Optional[EntityIdentity] = {}) -> EntityIdentity:
        return super(EntityIdentityResource, self)._create(opts)