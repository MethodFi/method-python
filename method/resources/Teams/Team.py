from typing import TypedDict, Optional, List, Literal, Union

from method.resource import MethodResponse, Resource, RequestOpts
from method.configuration import Configuration


TeamStatusesLiterals = Literal[
    'active',
    'verified',
    'disabled',
    'pending_disablement'
]


TeamContactTypesLiterals = Literal[
    'Admin',
    'Billing',
    'Technical'
]


class TeamContact(TypedDict):
    name: str
    email: str
    type: TeamContactTypesLiterals


class TeamAddress(TypedDict):
    line1: str
    line2: Optional[str]
    city: str
    state: str
    zipcode: str
    country: Optional[str]


class Team(TypedDict):
    id: str
    parent_id: Optional[str]
    name: str
    legal_name: str
    ein: str
    contacts: List[TeamContact]
    address: TeamAddress
    status: TeamStatusesLiterals
    logo: Optional[str]
    created_at: str
    updated_at: str


class TeamCreateOpts(TypedDict):
    name: str
    legal_name: str
    ein: str
    contacts: List[TeamContact]
    address: Optional[TeamAddress]


class TeamEncryptionKeyRSAKey(TypedDict):
    keyModulus: str
    keyExponent: str


class TeamEncryptionKeyCertificate(TypedDict):
    certificate: str


class TeamEncryptionKeyOpts(TypedDict):
    encryption_key: Union[TeamEncryptionKeyRSAKey, TeamEncryptionKeyCertificate]


MLEPublicKeyTypesLiterals = Literal[
    'direct',
    'well_known'
]


MLEPublicKeyStatusesLiterals = Literal[
    'active',
    'disabled'
]


class JWK(TypedDict):
    kid: Optional[str]
    kty: str
    alg: Optional[str]
    use: Optional[str]
    n: str
    e: str


class MLEPublicKey(TypedDict):
    id: str
    type: MLEPublicKeyTypesLiterals
    jwk: Optional[JWK]
    well_known_endpoint: Optional[str]
    status: MLEPublicKeyStatusesLiterals
    contact: str
    created_at: str
    updated_at: str


class MLEPublicKeyCreateOpts(TypedDict):
    type: MLEPublicKeyTypesLiterals
    contact: str
    jwk: Optional[JWK]
    well_known_endpoint: Optional[str]


class TeamMLEPublicKeysResource(Resource):
    def __init__(self, config: Configuration):
        super(TeamMLEPublicKeysResource, self).__init__(config.add_path('public_keys'))

    def create(self, opts: MLEPublicKeyCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[MLEPublicKey]:
        return super(TeamMLEPublicKeysResource, self)._create(opts, request_opts=request_opts)

    def list(self) -> MethodResponse[List[MLEPublicKey]]:
        return super(TeamMLEPublicKeysResource, self)._list(None)

    def retrieve(self, _id: str) -> MethodResponse[MLEPublicKey]:
        return super(TeamMLEPublicKeysResource, self)._get_with_id(_id)

    def delete(self, _id: str) -> MethodResponse[MLEPublicKey]:
        return super(TeamMLEPublicKeysResource, self)._delete(_id)


class TeamMLEResource(Resource):
    public_keys: TeamMLEPublicKeysResource

    def __init__(self, config: Configuration):
        _config = config.add_path('mle')
        super(TeamMLEResource, self).__init__(_config)
        self.public_keys = TeamMLEPublicKeysResource(_config)


class TeamResource(Resource):
    mle: TeamMLEResource

    def __init__(self, config: Configuration):
        _config = config.add_path('teams')
        super(TeamResource, self).__init__(_config)
        self.mle = TeamMLEResource(_config)

    def list(self) -> MethodResponse[List[Team]]:
        return super(TeamResource, self)._list(None)

    def create(self, opts: TeamCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[Team]:
        return super(TeamResource, self)._create(opts, request_opts=request_opts)

    def update_encryption_key(self, opts: TeamEncryptionKeyOpts) -> MethodResponse[None]:
        return super(TeamResource, self)._create_with_sub_path('default_encryption_key', opts)
