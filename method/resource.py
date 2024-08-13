from importlib.metadata import version
import json
from typing import Optional, List, Dict, Any, TypedDict, Literal, Union
from hammock import Hammock as Client  # type: ignore
from method.configuration import Configuration
from method.errors import MethodError


ResourceStatusLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]

class MethodResponse:
    def __init__(self, data: Any, last_response: Any):
        self._data = data
        self._last_response = last_response

    @property
    def last_response(self):
        return self._last_response
    
    def __getitem__(self, key):
        return self._data[key]

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'MethodResponse' object has no attribute '{name}'")

    def __repr__(self):
        return repr(self._data)

    def __iter__(self):
        return iter(self._data)

    def to_dict(self) -> Dict:
        return self._data

    def __dir__(self):
        """Override dir to hide last_response from autocomplete and dir() calls"""
        return [item for item in dir(self._data) if item != 'last_response']

    def __eq__(self, other):
        if isinstance(other, MethodResponse):
            return self._data == other._data and self._last_response == other._last_response
        return False

    def finalize_response(self, request_end_time: Optional[int] = None):
        """Sets the request end time."""
        if request_end_time is not None:
            self._last_response['request_end_time'] = request_end_time    

class LastResponse:
    def __init__(self, response: Any):
        self.last_response = {
            'request_id': response.headers.get('idem-request-id', None),
            'idempotency_status': response.headers.get('idem-status', None),
            # TODO: 'method'
            # TODO: 'path'
            # TODO: 'status'
            # TODO: 'request_start_time'
            'request_end_time': None,
            'pagination': self._extract_pagination_info(response.headers)
        }

    def _extract_pagination_info(self, headers: Dict[str, str]) -> Dict[str, Any]:
        pagination = {}
        if (headers.get('pagination-page')):
            pagination['page'] = headers.get('pagination-page')
        if (headers.get('pagination-page-count')):
            pagination['page_count'] = headers.get('pagination-page-count')
        if (headers.get('pagination-page-limit')):
            pagination['page_limit'] = headers.get('pagination-page-limit')
        if (headers.get('pagination-total-count')):
            pagination['total_count'] = headers.get('pagination-total-count')
        if (headers.get('pagination-page-cursor-next')):
            pagination['next_page'] = headers.get('pagination-page-cursor-next')
        if (headers.get('pagination-page-cursor-prev')):
            pagination['previous_page'] = headers.get('pagination-page-cursor-prev')

class RequestOpts(TypedDict):
    idempotency_key: Optional[str]


class ResourceListOpts(TypedDict):
    from_date: Optional[str]
    to_date: Optional[str]
    page: Optional[Union[int, str]]
    page_limit: Optional[Union[int, str]]
    page_cursor: Optional[Union[int, str]]


class Resource:
    config: Configuration
    client: Client

    def __init__(self, config: Configuration):
        self.config = config
        self.client = Client(config.url, headers={
            'Authorization': 'Bearer {token}'.format(token=config.api_key),
            'Content-Type': 'application/json',
            'User-Agent': 'Method-Python/v{version}'.format(version=version('method-python')),
            'method-version': '2024-04-04'
        })
    
    # def _make_request(self, method: str, path: Optional[str] = None, data: Optional[Dict] = None, params: Optional[Dict] = None, headers: Optional[Dict] = None, raw: bool = False) -> MethodResponse:
    #     client_path = self.client if not path else self.client(path)

    @MethodError.catch
    def _get_raw(self) -> Any:
        raw = self.client.GET()
        response = raw.json()
        last_response = LastResponse(raw).last_response
        return MethodResponse(response, last_response)

    @MethodError.catch
    def _get(self) -> Any:
        response = self.client.GET().json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _get_with_id(self, _id: str) -> Any:
        response = self.client.GET(_id).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _get_with_params(self, params: Dict) -> Any:
        response = self.client.GET(params=params).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _get_with_sub_path(self, path: str) -> Any:
        response = self.client(path).GET().json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _get_with_sub_path_and_params(self, path: str, params: Dict) -> Any:
        response = self.client(path).GET(params=params).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _list(self, params: Optional[Dict] = None) -> List[Any]:
        response = self.client.GET(params=params).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _create(self, data: Dict, request_opts: Optional[RequestOpts] = None) -> Any:
        opts = {'headers': {}}
        if request_opts and request_opts.get('idempotency_key'):
            opts['headers']['Idempotency-Key'] = request_opts.get('idempotency_key')

        response = self.client.POST(data=json.dumps(data), **opts).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _create_with_sub_path(self, path: str, data: Dict) -> Any:
        response = self.client(path).POST(data=json.dumps(data)).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _update_with_id(self, _id: str, data: Dict) -> Any:
        response = self.client(_id).PUT(data=json.dumps(data)).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _update(self, data: Dict) -> Any:
        response = self.client.PUT(data=json.dumps(data)).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _update_with_sub_path(self, path: str, data: Dict) -> Any:
        response = self.client(path).PUT(data=json.dumps(data)).json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _delete(self, _id: str) -> Any:
        response = self.client(_id).DELETE().json()
        return MethodResponse(response.get('data'), response)
   
    @MethodError.catch
    def _delete_with_sub_path(self, path: str) -> Any:
        response = self.client(path).DELETE().json()
        return MethodResponse(response.get('data'), response)

    @MethodError.catch
    def _download(self, _id: str) -> str:
        response = self.client(_id).download.GET()
        return MethodResponse(response.text, response)

    @MethodError.catch
    def _post_with_id(self, _id: str, data: Dict) -> Any:
        response = self.client(_id).POST(data=json.dumps(data)).json()
        return MethodResponse(response.get('data'), response)
