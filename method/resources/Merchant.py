from typing import TypedDict, Optional, List, Union

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Accounts.Types import AccountLiabilityTypesLiterals


class MerchantProviderIds(TypedDict):
    plaid: List[str]
    mx: List[str]
    finicity: List[str]
    dpp: List[str]
    rpps: List[str]


class Merchant(TypedDict):
    id: str
    parent_name: str
    name: str
    logo: str
    type: AccountLiabilityTypesLiterals
    provider_ids: MerchantProviderIds
    is_temp: bool
    account_number_formats: List[str]

MerchantListOpts = TypedDict('MerchantListOpts', {
    'page': Optional[Union[str, int]],
    'page_limit': Optional[Union[str, int]],
    'type': Optional[AccountLiabilityTypesLiterals],
    'name': Optional[str],
    'creditor_name': Optional[str],
    'provider_id.plaid': Optional[str],
    'provider_id.mx': Optional[str],
    'provider_id.finicity': Optional[str],
    'provider_id.dpp': Optional[str]
})


class MerchantResource(Resource):
    def __init__(self, config: Configuration):
        super(MerchantResource, self).__init__(config.add_path('merchants'))

    def retrieve(self, _id: str) -> MethodResponse[Merchant]:
        return super(MerchantResource, self)._get_with_id(_id)

    def list(self, opts: Optional[MerchantListOpts] = None) -> MethodResponse[List[Merchant]]:
        return super(MerchantResource, self)._list(opts)
