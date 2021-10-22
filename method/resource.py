import json
from typing import Optional, List, Dict, Any, TypedDict
from hammock import Hammock as Client  # type: ignore
from method.configuration import Configuration
from method.errors import MethodError


class RequestOpts(TypedDict):
    idempotency_key: Optional[str]


class Resource:
    config: Configuration
    client: Client

    def __init__(self, config: Configuration):
        self.config = config
        self.client = Client(config.url, headers={
            'Authorization': 'Bearer {token}'.format(token=config.api_key),
            'Content-Type': 'application/json'
        })

    @MethodError.catch
    def _get_raw(self) -> Any:
        return self.client.GET().json()

    @MethodError.catch
    def _get(self) -> Any:
        return self.client.GET().json().get('data')

    @MethodError.catch
    def _get_with_id(self, _id: str) -> Any:
        return self.client.GET(_id).json().get('data')

    @MethodError.catch
    def _get_with_params(self, params: Dict) -> Any:
        return self.client.GET(params=params).json().get('data')

    @MethodError.catch
    def _get_with_sub_path(self, path: str) -> Any:
        return self.client(path).GET().json().get('data')

    @MethodError.catch
    def _list(self, params: Optional[Dict] = None) -> List[Any]:
        return self.client.GET(params=params).json().get('data')

    @MethodError.catch
    def _create(self, data: Dict, request_opts: Optional[RequestOpts] = None) -> Any:
        opts = {'headers': {}}
        if request_opts and request_opts.get('idempotency_key'):
            opts['headers']['Idempotency-Key'] = request_opts.get('idempotency_key')

        return self.client.POST(data=json.dumps(data), **opts).json().get('data')

    @MethodError.catch
    def _create_with_sub_path(self, path: str, data: Dict) -> Any:
        return self.client(path).POST(data=json.dumps(data)).json().get('data')

    @MethodError.catch
    def _update_with_id(self, _id: str, data: Dict) -> Any:
        return self.client(_id).PUT(data=json.dumps(data)).json().get('data')

    @MethodError.catch
    def _update(self, data: Dict) -> Any:
        return self.client.PUT(data=json.dumps(data)).json().get('data')

    @MethodError.catch
    def _delete(self, _id: str) -> Any:
        return self.client(_id).DELETE().json().get('data')

    @MethodError.catch
    def _download(self, _id: str) -> str:
        return self.client(_id).download.GET().text
