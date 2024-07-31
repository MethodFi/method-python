from method.resource import Resource
from method.configuration import Configuration
from method.resources.Elements.Token import ElementTokenResource


class ElementResource(Resource):
    token: ElementTokenResource

    def __init__(self, config: Configuration):
        _config = config.add_path('elements')
        super(ElementResource, self).__init__(_config)
        self.token = ElementTokenResource(_config)
