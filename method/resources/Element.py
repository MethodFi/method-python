from typing import TypedDict, Optional, Literal, List

from method.resource import Resource
from method.configuration import Configuration
from method.resources.Account import Account


ElementTypesLiterals = Literal['link']


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


class ElementExchangePublicAccountOpts(TypedDict):
    public_account_token: Optional[str]
    public_account_tokens: Optional[List[str]]


class ElementResource(Resource):
    def __init__(self, config: Configuration):
        super(ElementResource, self).__init__(config.add_path('elements'))

    def create_token(self, opts: ElementTokenCreateOpts) -> Element:
        return super(ElementResource, self)._create_with_sub_path('/token', opts)

    def exchange_public_account_token(self, opts: ElementExchangePublicAccountOpts) -> Account:
        return super(ElementResource, self)._create_with_sub_path('/accounts/exchange', opts)

    def exchange_public_account_tokens(self, opts: ElementExchangePublicAccountOpts) -> Account:
        return super(ElementResource, self)._create_with_sub_path('/accounts/exchange', opts)
