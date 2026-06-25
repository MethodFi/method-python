from typing import TypedDict, Optional, List, Dict, Any, Literal

from method.resource import MethodResponse, Resource, RequestOpts, ResourceListOpts
from method.configuration import Configuration


SecretStatusesLiterals = Literal[
    'active',
    'deleted'
]


class Secret(TypedDict):
    id: str
    metadata: Optional[Dict[str, Any]]
    status: SecretStatusesLiterals
    created_at: str
    updated_at: str


class SecretCreateOpts(TypedDict):
    value: str
    metadata: Optional[Dict[str, Any]]


class SecretResource(Resource):
    def __init__(self, config: Configuration):
        super(SecretResource, self).__init__(config.add_path('secrets'))

    def retrieve(self, _id: str) -> MethodResponse[Secret]:
        return super(SecretResource, self)._get_with_id(_id)

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[Secret]]:
        return super(SecretResource, self)._list(params)

    def create(self, opts: SecretCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[Secret]:
        return super(SecretResource, self)._create(opts, request_opts)

    def delete(self, _id: str) -> MethodResponse[Secret]:
        return super(SecretResource, self)._delete(_id)
