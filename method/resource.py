import time
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

    # @property
    # def last_response(self):
    #     return self._last_response
    
    # def __getitem__(self, key):
    #     return self._data[key]

    # def __getattr__(self, name):
    #     if name in self._data:
    #         return self._data[name]
    #     raise AttributeError(f"'MethodResponse' object has no attribute '{name}'")

    # def __repr__(self):
    #     return repr(self._data)

    # def __iter__(self):
    #     return iter(self._data)

    # def to_dict(self) -> Dict:
    #     return self._data

    # def __dir__(self):
    #     """Override dir to hide last_response from autocomplete and dir() calls"""
    #     return [item for item in dir(self._data) if item != 'last_response']

    # def __eq__(self, other):
    #     if isinstance(other, MethodResponse):
    #         return self._data == other._data and self._last_response == other._last_response
    #     return False

    def finalize_response(self, request_start_time: Optional[int] = None, request_end_time: Optional[int] = None):
        if request_start_time is not None:
            self._last_response['request_start_time'] = request_start_time
        if request_end_time is not None:
            self._last_response['request_end_time'] = request_end_time    

class LastResponse:
    def __init__(self, response: Any):
        self.last_response = {
            'request_id': response.headers.get('idem-request-id', None),
            'idempotency_status': response.headers.get('idem-status', None),
            'method': response.request.method,
            'path': response.request.path_url,
            'status': response.status_code,
            'request_start_time': None,
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
    
    def _make_request(self, method: str, path: Optional[str] = None, data: Optional[Dict] = None, params: Optional[Dict] = None, headers: Optional[Dict] = None, raw: bool = False) -> MethodResponse:
        client_path = self.client if not path else self.client(path)
        request_method = getattr(client_path, method)

        options = {}
        if data:
            options['data'] = json.dumps(data)
        if params:
            options['params'] = params
        if headers:
            options['headers'] = headers

        request_start_time = int(time.time() * 1000)
        raw_response = request_method(**options)
        request_end_time = int(time.time() * 1000)

        last_response = LastResponse(raw_response).last_response

        if raw:
            response = MethodResponse(raw_response.json(), last_response)
            response.finalize_response(request_start_time, request_end_time)
            return response
        else:
            response = MethodResponse(raw_response.json().get('data'), last_response)
            response.finalize_response(request_start_time, request_end_time)
            return response


    @MethodError.catch
    def _get_raw(self) -> Any:
        return self._make_request('GET', raw=True)

    @MethodError.catch
    def _get(self) -> Any:
        return self._make_request('GET')

    @MethodError.catch
    def _get_with_id(self, _id: str) -> Any:
        return self._make_request('GET', path=_id)

    @MethodError.catch
    def _get_with_params(self, params: Dict) -> Any:
        return self._make_request('GET', params=params)

    @MethodError.catch
    def _get_with_sub_path(self, path: str) -> Any:
        return self._make_request('GET', path=path)

    @MethodError.catch
    def _get_with_sub_path_and_params(self, path: str, params: Dict) -> Any:
        return self._make_request('GET', path=path, params=params)

    @MethodError.catch
    def _list(self, params: Optional[Dict] = None) -> List[Any]:
        return self._make_request('GET', params=params)

    @MethodError.catch
    def _create(self, data: Dict, request_opts: Optional[RequestOpts] = None) -> Any:
        headers = {}
        if request_opts and request_opts.get('idempotency_key'):
            headers['Idempotency-Key'] = request_opts.get('idempotency_key')
        return self._make_request('POST', data=data, headers=headers)

    @MethodError.catch
    def _create_with_sub_path(self, path: str, data: Dict) -> Any:
        return self._make_request('POST', path=path, data=data)

    @MethodError.catch
    def _update_with_id(self, _id: str, data: Dict) -> Any:
        return self._make_request('PUT', path=_id, data=data)

    @MethodError.catch
    def _update(self, data: Dict) -> Any:
        return self._make_request('PUT', data=data)

    @MethodError.catch
    def _update_with_sub_path(self, path: str, data: Dict) -> Any:
        return self._make_request('PUT', path=path, data=data)

    @MethodError.catch
    def _delete(self, _id: str) -> Any:
        return self._make_request('DELETE', path=_id)
   
    @MethodError.catch
    def _delete_with_sub_path(self, path: str) -> Any:
        return self._make_request('DELETE', path=path)

    @MethodError.catch
    def _download(self, _id: str) -> str:
        return self._make_request('GET', path=_id).content #FIXME: This should return a file

    @MethodError.catch
    def _post_with_id(self, _id: str, data: Dict) -> Any:
        return self._make_request('POST', path=_id, data=data)
