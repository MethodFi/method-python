from typing import TypedDict, Optional, Literal

from method.resource import Resource
from method.configuration import Configuration


RoutingNumberOfficeTypesLiterals = Literal[
    'main',
    'branch'
]


class RoutingNumberAddress(TypedDict):
    line1: str
    line2: Optional[str]
    city: str
    state: str
    zip: str


class RoutingNumber(TypedDict):
    id: str
    institution_name: str
    routing_number: str
    logo: str
    office_type: RoutingNumberOfficeTypesLiterals
    change_date: str
    address: RoutingNumberAddress
    phone: Optional[str]


class RoutingNumberResource(Resource):
    def __init__(self, config: Configuration):
        super(RoutingNumberResource, self).__init__(config.add_path('routing_numbers'))

    def get(self, routing_number: str) -> RoutingNumber:
        return super(RoutingNumberResource, self)._get_with_params({'routing_number': routing_number})
