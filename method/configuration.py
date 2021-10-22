from copy import deepcopy
from typing import TypedDict, Optional, Literal


EnvironmentLiterals = Literal[
    'dev',
    'sandbox',
    'production'
]

Environments = [
    'dev',
    'sandbox',
    'production'
]


class ConfigurationOpts(TypedDict):
    api_key: str
    env: Optional[EnvironmentLiterals]


class Configuration:
    api_key: str
    url: str
    env: EnvironmentLiterals

    def __init__(self, opts: ConfigurationOpts):
        url = 'https://{env}.methodfi.com'

        self.__validate(opts)
        self.api_key = opts.get('api_key', '')
        self.url = url.format(env=opts.get('env', 'dev'))

    def add_path(self, path: str):
        copy = deepcopy(self)
        copy.url = '{url}/{path}'.format(url=self.url, path=path)
        return copy

    @staticmethod
    def __validate(opts):
        if opts.get('env') not in Environments:
            raise KeyError('Invalid env: {env}'.format(env=opts.get('env')))

        if 'api_key' not in opts:
            raise KeyError('Missing key: api_key')
