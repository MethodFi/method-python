from typing import TypedDict, Optional, List, Literal, Union

from method.resource import MethodResponse, Resource
from method.configuration import Configuration


MerchantTypesLiterals = Literal[
    'auto_loan',
    'business_loan',
    'credit_card',
    'electric_utility',
    'home_loan',
    'insurance',
    'internet_utility',
    'loan',
    'medical',
    'personal_loan',
    'student_loan',
    'telephone_utility',
    'television_utility',
    'water_utility',
    'bank',
    'home_equity_loan',
    'mortgage',
    'utility',
    'waste_utility',
    'collection'
    'credit_builder',
]


class MerchantProviderIds(TypedDict):
    plaid: List[str]
    mx: List[str]
    finicity: List[str]


class Merchant(TypedDict):
    mch_id: str
    parent_name: str
    name: str
    logo: str
    description: Optional[str]
    note: Optional[str]
    types: List[MerchantTypesLiterals]
    account_prefixes: List[str]
    provider_ids: MerchantProviderIds
    customized_auth: bool
    is_temp: bool

MerchantListOpts = TypedDict('MerchantListOpts', {
    'page': Optional[Union[str, int]],
    'page_limit': Optional[Union[str, int]],
    'type': Optional[MerchantTypesLiterals],
    'name': Optional[str],
    'provider_id.plaid': Optional[str],
    'provider_id.mx': Optional[str],
    'provider_id.finicity': Optional[str]
})


class MerchantResource(Resource):
    def __init__(self, config: Configuration):
        super(MerchantResource, self).__init__(config.add_path('merchants'))

    def retrieve(self, _id: str) -> MethodResponse[Merchant]:
        return super(MerchantResource, self)._get_with_id(_id)

    def list(self, opts: Optional[MerchantListOpts] = None) -> MethodResponse[List[Merchant]]:
        return super(MerchantResource, self)._list(opts)
