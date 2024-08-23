from typing import TypedDict, Literal

from method.resource import MethodResponse, Resource
from method.configuration import Configuration


class PingResponse(TypedDict):
    success: bool
    data: None
    message: Literal['pong']


class HealthCheckResource(Resource):
    def __init__(self, config: Configuration):
        super(HealthCheckResource, self).__init__(config.add_path('ping'))

    def retrieve(self) -> MethodResponse[PingResponse]:
        return super(HealthCheckResource, self)._get_raw()
