from typing import TypedDict, Optional, Dict, Any, List, Literal
from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration
from method.resources.Webhook import WebhookTypesLiterals

EventResourceTypesLiterals = Literal[
    'account',
    'credit_score',
    'attribute',
    'connect'
]

class EventDiff(TypedDict):
    before: Optional[Dict[str, Any]]
    after: Optional[Dict[str, Any]]

class Event(TypedDict):
    id: str
    type: WebhookTypesLiterals
    resource_id: str
    resource_type: EventResourceTypesLiterals
    data: Dict[str, Any]
    diff: EventDiff
    updated_at: str
    created_at: str

class EventListOpts(ResourceListOpts):
    resource_id: Optional[str]
    resource_type: Optional[EventResourceTypesLiterals]
    type: Optional[WebhookTypesLiterals]

class EventResource(Resource):
    def __init__(self, config: Configuration):
        super(EventResource, self).__init__(config.add_path('events'))

    def retrieve(self, evt_id: str) -> MethodResponse[Event]:
        return super(EventResource, self)._get_with_id(evt_id)

    def list(self, params: Optional[EventListOpts] = None) -> MethodResponse[List[Event]]:
        return super(EventResource, self)._list(params)