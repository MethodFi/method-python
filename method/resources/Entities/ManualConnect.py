from typing import TypedDict, Optional, Literal, List

from method.resource import MethodResponse, Resource, RequestOpts
from method.configuration import Configuration
from method.resources.Entities.Connect import EntityConnect


ManualConnectBureausLiterals = Literal[
    'equifax',
    'transunion'
]


class ManualConnectNarrativeCode(TypedDict):
    code: Optional[str]
    description: Optional[str]


class ManualConnectTradeline(TypedDict):
    type_code: Optional[str]
    portfolio_type_code: Optional[str]
    designator_code: Optional[str]
    number: Optional[str]
    creditor_name: Optional[str]
    creditor_code: Optional[str]
    balance: Optional[int]
    highest_balance: Optional[int]
    credit_limit: Optional[int]
    term: Optional[int]
    next_payment_minimum_amount: Optional[int]
    last_payment_amount: Optional[int]
    payment_history: Optional[List[str]]
    past_due_amount: Optional[int]
    delinquency_charge_off_amount: Optional[int]
    opened_at: Optional[str]
    closed_at: Optional[str]
    last_activity_date: Optional[str]
    reported_date: Optional[str]
    next_payment_due_date: Optional[str]
    last_payment_date: Optional[str]
    delinquency_first_start_date: Optional[str]
    narrative_codes: Optional[List[ManualConnectNarrativeCode]]
    external_id: Optional[str]


class ManualConnectCreateOpts(TypedDict):
    bureau: ManualConnectBureausLiterals
    tradelines: List[ManualConnectTradeline]


class EntityManualConnectResource(Resource):
    def __init__(self, config: Configuration):
        super(EntityManualConnectResource, self).__init__(config.add_path('manual_connect'))

    def retrieve(self, mcxn_id: str) -> MethodResponse[EntityConnect]:
        return super(EntityManualConnectResource, self)._get_with_id(mcxn_id)

    def create(self, opts: ManualConnectCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[EntityConnect]:
        return super(EntityManualConnectResource, self)._create(opts, request_opts=request_opts)
