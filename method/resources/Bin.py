from typing import TypedDict, Optional, Literal

from method.resource import Resource
from method.configuration import Configuration


BinBrandsLiterals = Literal[
    'amex',
    'visa',
    'mastercard',
    'discover',
    'diners_club'
]

BinTypesLiterals = Literal['debit', 'credit']


class Bin(TypedDict):
    id: Optional[str]
    bin: Optional[str]
    brand: BinBrandsLiterals
    issuer: Optional[str]
    type: Optional[BinTypesLiterals]
    category: Optional[str]
    bank_url: Optional[str]
    sample_pan: Optional[str]


class BinResource(Resource):
    def __init__(self, config: Configuration):
        super(BinResource, self).__init__(config.add_path('bins'))

    def get(self, _id: str) -> Bin:
        return super(BinResource, self)._get_with_params({'bin': _id})
