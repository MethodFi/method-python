from typing import TypedDict, Optional, Dict, Any, Literal

from method.resource import Resource, RequestOpts
from method.configuration import Configuration


ReportTypesLiterals = Literal[
    'payments.created.current',
    'payments.created.previous',
    'payments.updated.current',
    'payments.updated.previous'
]


ReportStatusesLiterals = Literal[
    'processing',
    'completed'
]


class Report(TypedDict):
    id: str
    type: ReportTypesLiterals
    url: str
    status: ReportStatusesLiterals
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str


class ReportCreateOpts(TypedDict):
    type: ReportTypesLiterals
    metadata: Optional[Dict[str, Any]]


class ReportResource(Resource):
    def __init__(self, config: Configuration):
        super(ReportResource, self).__init__(config.add_path('reports'))

    def get(self, _id: str) -> Report:
        return super(ReportResource, self)._get_with_id(_id)

    def create(self, opts: ReportCreateOpts, request_opts: Optional[RequestOpts] = None) -> Report:
        return super(ReportResource, self)._create(opts, request_opts)

    def download(self, _id: str) -> str:
        return super(ReportResource, self)._download(_id)
