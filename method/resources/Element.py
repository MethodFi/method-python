from typing import TypedDict, Optional, Literal, List, Dict

from method.resource import Resource
from method.configuration import Configuration
from method.resources.Account import Account


ElementTypesLiterals = Literal[
    'link'
]


UserEventTypeLiterals = Literal[
    'auth_intro_open',
    'auth_intro_continue',
    'auth_intro_close',
    'auth_name_open',
    'auth_name_continue',
    'auth_name_close',
    'auth_phone_open',
    'auth_phone_continue',
    'auth_phone_close',
    'auth_phone_verify_open',
    'auth_phone_verify_submit',
    'auth_phone_verify_close',
    'auth_dob_open',
    'auth_dob_continue',
    'auth_dob_close',
    'auth_address_open',
    'auth_address_continue',
    'auth_address_close',
    'auth_incorrect_info_open',
    'auth_incorrect_info_try_again',
    'auth_invalid_info_open',
    'auth_invalid_info_exit',
    'auth_secq_open',
    'auth_secq_continue',
    'auth_secq_close',
    'auth_secq_incorrect_open',
    'auth_secq_incorrect_try_again',
    'auth_secq_incorrect_close',
    'auth_consent_open',
    'auth_consent_continue',
    'auth_consent_close',
    'auth_success_open',
    'auth_success_continue',
    'auth_failure_open',
    'auth_failure_continue'
]


class LinkElementLinkCreateOpts(TypedDict):
    mch_id: Optional[str]
    mask: Optional[str]


class ElementTokenCreateOpts(TypedDict):
    entity_id: str
    type: ElementTypesLiterals
    team_name: Optional[str]
    link: Optional[LinkElementLinkCreateOpts]


class Element(TypedDict):
    element_token: str


class ElementUserEvent(TypedDict):
    type: UserEventTypeLiterals
    timestamp: str
    metadata: Optional[Dict[str, any]]

class TokenSessionResult(TypedDict):
    authenticated: bool
    cxn_id: Optional[str]
    accounts: List[str]
    entity_id: Optional[str]
    events: List[ElementUserEvent]


class ElementExchangePublicAccountOpts(TypedDict):
    public_account_token: Optional[str]
    public_account_tokens: Optional[List[str]]


class ElementResource(Resource):
    def __init__(self, config: Configuration):
        super(ElementResource, self).__init__(config.add_path('elements'))

    def create_token(self, opts: ElementTokenCreateOpts) -> Element:
        return super(ElementResource, self)._create_with_sub_path('token', opts)
    
    def get_session_results(self, _id: str) -> TokenSessionResult:
        return super(ElementResource, self)._get_with_sub_path('token/{_id}/results'.format(_id=_id))

    def exchange_public_account_token(self, opts: ElementExchangePublicAccountOpts) -> Account:
        return super(ElementResource, self)._create_with_sub_path('accounts/exchange', opts)

    def exchange_public_account_tokens(self, opts: ElementExchangePublicAccountOpts) -> Account:
        return super(ElementResource, self)._create_with_sub_path('accounts/exchange', opts)
