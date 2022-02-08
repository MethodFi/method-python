from typing import TypedDict, List, Literal, Dict, Any, Optional

from method.resource import Resource
from method.configuration import Configuration
from method.errors import ResourceError


ReversalStatusesLiterals = Literal[
    'pending_approval',
    'pending',
    'processing',
    'sent',
    'failed'
]


ReversalDirectionsLiterals = Literal[
    'debit',
    'credit'
]


class Reversal(TypedDict):
    id: str
    pmt_id: str
    target_account: str
    trace_id: Optional[str]
    direction: ReversalDirectionsLiterals
    description: str
    amount: int
    status: ReversalStatusesLiterals
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class ReversalUpdateOpts(TypedDict):
    status: ReversalStatusesLiterals
    description: Optional[str]


class ReversalResource(Resource):
    def __init__(self, config: Configuration):
        super(ReversalResource, self).__init__(config.add_path('reversals'))

    def get(self, _id: str) -> Reversal:
        return super(ReversalResource, self)._get_with_id(_id)

    def update(self, _id: str, opts: ReversalUpdateOpts) -> Reversal:
        return super(ReversalResource, self)._update_with_id(_id, opts)

    def list(self) -> List[Reversal]:
        return super(ReversalResource, self)._list(None)
