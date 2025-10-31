from method.resource import Resource
from method.configuration import Configuration
from method.resources.Opal.Token import OpalTokenResource


class OpalResource(Resource):
    token: OpalTokenResource

    def __init__(self, config: Configuration):
        _config = config.add_path('opal')
        super(OpalResource, self).__init__(_config)
        self.token = OpalTokenResource(_config)
