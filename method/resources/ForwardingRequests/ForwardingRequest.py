from typing import TypedDict, Optional, Dict, Any, Literal, List

from method.resource import MethodResponse, Resource, RequestOpts
from method.configuration import Configuration


ForwardingRequestStatusesLiterals = Literal[
    'completed',
    'failed'
]

ForwardingRequestMethodsLiterals = Literal[
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE'
]


class ForwardingRequestDetail(TypedDict):
    url: str
    method: ForwardingRequestMethodsLiterals
    headers: Dict[str, str]
    body: str


class ForwardingResponseDetail(TypedDict):
    status_code: Optional[int]
    headers: Dict[str, str]
    body: Optional[Any]


class ForwardingRequest(TypedDict):
    id: str
    bindings: Dict[str, str]
    request: ForwardingRequestDetail
    response: ForwardingResponseDetail
    duration_ms: float
    status: ForwardingRequestStatusesLiterals
    status_history: List[Dict[str, Any]]
    created_at: str


class ForwardingRequestCreateOpts(TypedDict):
    url: str
    method: ForwardingRequestMethodsLiterals
    headers: Dict[str, str]
    body: str
    bindings: Dict[str, str]
    metadata: Optional[Dict[str, Any]]


class ForwardingRequestResource(Resource):
    def __init__(self, config: Configuration):
        super(ForwardingRequestResource, self).__init__(config.add_path('forwarding_requests'))

    def retrieve(self, freq_id: str) -> MethodResponse[ForwardingRequest]:
        return super(ForwardingRequestResource, self)._get_with_id(freq_id)

    def create(self, opts: ForwardingRequestCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[ForwardingRequest]:
        return super(ForwardingRequestResource, self)._create(opts, request_opts=request_opts)
