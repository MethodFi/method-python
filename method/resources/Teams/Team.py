from typing import TypedDict, Optional, Dict, Any, Literal, List

from method.resource import MethodResponse, Resource, RequestOpts
from method.configuration import Configuration


TeamStatusesLiterals = Literal[
    'active',
    'verified',
    'disabled',
    'pending_disablement'
]


class TeamProduct(TypedDict):
    type: str
    enabled: bool


class TeamKey(TypedDict):
    id: str
    type: Literal['secret', 'public']
    deleted: bool
    created_at: str
    updated_at: str
    last_used_at: Optional[str]


class Team(TypedDict):
    id: str
    parent_id: Optional[str]
    name: str
    legal_name: str
    logo: Optional[str]
    api_version: str
    status: TeamStatusesLiterals
    products: List[TeamProduct]
    keys: List[TeamKey]
    created_at: str
    updated_at: str


class TeamCreateOpts(TypedDict):
    name: str


class TeamEncryptionKeyOpts(TypedDict):
    key: str


class MLEPublicKey(TypedDict):
    id: str
    jwk: Dict[str, Any]
    created_at: str
    updated_at: str


class MLEPublicKeyCreateOpts(TypedDict):
    jwk: Dict[str, Any]


class TeamPublicKeysResource(Resource):
    def __init__(self, config: Configuration):
        super(TeamPublicKeysResource, self).__init__(config.add_path('mle/public_keys'))

    def list(self) -> MethodResponse[List[MLEPublicKey]]:
        return super(TeamPublicKeysResource, self)._list()

    def retrieve(self, key_id: str) -> MethodResponse[MLEPublicKey]:
        return super(TeamPublicKeysResource, self)._get_with_id(key_id)

    def create(self, opts: MLEPublicKeyCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[MLEPublicKey]:
        return super(TeamPublicKeysResource, self)._create(opts, request_opts)

    def delete(self, key_id: str) -> MethodResponse[MLEPublicKey]:
        return super(TeamPublicKeysResource, self)._delete(key_id)


class TeamResource(Resource):
    public_keys: TeamPublicKeysResource

    def __init__(self, config: Configuration):
        super(TeamResource, self).__init__(config.add_path('teams'))
        self.public_keys = TeamPublicKeysResource(self.config)

    def retrieve(self) -> MethodResponse[Team]:
        return super(TeamResource, self)._get()

    def create(self, opts: TeamCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[Team]:
        return super(TeamResource, self)._create(opts, request_opts)

    def update_encryption_key(self, opts: TeamEncryptionKeyOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[Team]:
        return super(TeamResource, self)._create_with_sub_path('default_encryption_key', opts)
