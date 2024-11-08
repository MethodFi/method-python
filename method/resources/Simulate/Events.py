from typing import Dict, TypedDict, Optional
from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Webhook import WebhookTypesLiterals

class SimulateEventsOpts(TypedDict):
    type: WebhookTypesLiterals
    entity_id: Optional[str]
    account_id: Optional[str]

class SimulateEventsResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateEventsResource, self).__init__(config.add_path('events'))

    def create(self, opts: SimulateEventsOpts) -> MethodResponse[Dict]:
        return super(SimulateEventsResource, self)._create(opts)