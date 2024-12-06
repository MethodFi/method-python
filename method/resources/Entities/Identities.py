from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Entities.Types import EntityIdentityType


EntityVerificationSessionStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


class EntityIdentity(TypedDict):
    id: str
    status: EntityVerificationSessionStatusLiterals
    identities: List[EntityIdentityType]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class EntityIdentityResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityIdentityResource, self).__init__(config.add_path('identities'))

    def retrieve(self, identity_id: str) -> MethodResponse[EntityIdentity]:
        return super(EntityIdentityResource, self)._get_with_id(identity_id)
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[EntityIdentity]]:
        return super(EntityIdentityResource, self)._list(params)

    def create(self, opts: Optional[EntityIdentityType] = {}) -> MethodResponse[EntityIdentity]:  # pylint: disable=dangerous-default-value
        return super(EntityIdentityResource, self)._create(opts)
