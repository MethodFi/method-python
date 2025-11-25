from typing import TypedDict, Literal

MethodErrorTypesLiterals = Literal[
    'INVALID_AUTHORIZATION',
    'INVALID_REQUEST',
    'API_ERROR'
]

class MethodErrorOpts(TypedDict):
    type: MethodErrorTypesLiterals
    sub_type: str
    message: str
    code: str

class MethodError(BaseException):
    type: MethodErrorTypesLiterals
    sub_type: str
    message: str
    code: str

    def __init__(self, opts: MethodErrorOpts):
        super(MethodError, self).__init__()

        self.type = opts.get('type', 'API_ERROR')
        self.sub_type = opts.get('sub_type', '')
        self.message = opts.get('message', '')
        self.code = opts.get('code', '')

    @staticmethod
    def catch(fn):
        def wrapper(*args, **kwargs):
            res = fn(*args, **kwargs)
            if (res is not None) and ('error' in res) and ('id' not in res):
                raise MethodError.generate(res['error'])
            return res
        return wrapper

    @staticmethod
    def generate(opts: MethodErrorOpts):
        error_type = opts.get('type')

        if error_type == 'INVALID_AUTHORIZATION':
            return MethodAuthorizationError(opts)
        if error_type == 'INVALID_REQUEST':
            return MethodInvalidRequestError(opts)
        if error_type == 'API_ERROR':
            return MethodInternalError(opts)

        # Default to MethodError for unknown error types
        return MethodError(opts)



class MethodInternalError(MethodError):
    pass


class MethodInvalidRequestError(MethodError):
    pass


class MethodAuthorizationError(MethodError):
    pass


class MethodHTTPError(MethodError):
    pass


class MethodBadRequestError(MethodError):
    pass


class MethodServerError(MethodError):
    pass

def from_status_code(status, opts):


    if 400 <= status < 500:
        return MethodBadRequestError(opts)
    if 500 <= status < 600:
        return MethodServerError(opts)
    return MethodError(opts)




class ResourceError(TypedDict):
    type: str
    sub_type: str
    message: str
    code: str

ERROR_CLASS_MAP = {
    'API_ERROR': MethodInternalError,
    'INVALID_REQUEST': MethodInvalidRequestError,
    'INVALID_AUTHORIZATION': MethodAuthorizationError
}

def build_method_error(opts: MethodErrorOpts) -> MethodError:
    cls = ERROR_CLASS_MAP.get(opts.get('type'), MethodError)
    return cls(opts)