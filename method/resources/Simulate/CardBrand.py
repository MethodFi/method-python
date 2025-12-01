from typing import TypedDict
from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Accounts.CardBrands import AccountCardBrand


class SimulateCardBrandOpts(TypedDict):
    brand_id: str


class SimulateCardBrandResource(Resource):
    def __init__(self, config: Configuration):
        super(SimulateCardBrandResource, self).__init__(config.add_path('card_brands'))

    def create(self, opts: SimulateCardBrandOpts) -> MethodResponse[AccountCardBrand]:
        """
        Simulate a Card Brand for a Credit Card Account.
        Card Brand simulation is available for Credit Card Accounts that have been verified
        and are subscribed to the Card Brands product.
        https://docs.methodfi.com/reference/simulations/card-brands/create

        Args:
            opts: SimulateCardBrandOpts containing brand_id
        """
        return super(SimulateCardBrandResource, self)._create(opts)
