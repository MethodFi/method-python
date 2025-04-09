from typing import TypedDict, Optional, Dict, List, Any, Literal, Union, TypeVar
from method.resource import MethodResponse, Resource, RequestOpts
from method.errors import ResourceError
from method.configuration import Configuration
from method.resources.Accounts.Types import AccountACH, AccountStatusesLiterals, AccountTypesLiterals, \
    AccountProductTypesLiterals, AccountSubscriptionTypesLiterals, AccountExpandableFieldsLiterals, \
    AccountLiability
from method.resources.Accounts.Balances import AccountBalance, AccountBalancesResource
from method.resources.Accounts.CardBrands import AccountCardBrand, AccountCardBrandsResource
from method.resources.Accounts.Payoffs import AccountPayoff, AccountPayoffsResource
from method.resources.Accounts.Sensitive import AccountSensitive, AccountSensitiveResource
from method.resources.Accounts.Subscriptions import AccountSubscriptionsResource
from method.resources.Accounts.Transactions import AccountTransaction, AccountTransactionsResource
from method.resources.Accounts.Updates import AccountUpdate, AccountUpdatesResource
from method.resources.Accounts.VerificationSessions import AccountVerificationSession, AccountVerificationSessionResource
from method.resources.Accounts.Products import AccountProduct, AccountProductResource
from method.resources.Accounts.Attributes import AccountAttributes, AccountAttributesResource
from method.resources.Accounts.PaymentInstruments import AccountPaymentInstrument, AccountPaymentInstrumentsResource

class AccountCreateOpts(TypedDict):
    holder_id: str
    metadata: Optional[Dict[str, Any]]


class AccountACHCreateOpts(AccountCreateOpts):
    ach: AccountACH


class LiabilityCreateOpts(TypedDict):
    mch_id: str
    account_number: Optional[str]
    number: Optional[str]


class AccountLiabilityCreateOpts(AccountCreateOpts):
    liability: LiabilityCreateOpts


AccountListOpts = TypedDict('AccountListOpts', {
    'to_date': Optional[str],
    'from_date': Optional[str],
    'page': Optional[int],
    'page_limit': Optional[int],
    'page_cursor': Optional[str],
    'status': Optional[str],
    'type': Optional[str],
    'holder_id': Optional[str],
    'expand': Optional[List[AccountExpandableFieldsLiterals]],
    'liability.mch_id': Optional[str],
    'liability.type': Optional[str]
})


class Account(TypedDict):
    id: str
    holder_id: str
    status: AccountStatusesLiterals
    type: AccountTypesLiterals
    ach: Optional[AccountACH]
    liability: Optional[AccountLiability]
    products: List[AccountProductTypesLiterals]
    restricted_products: List[AccountProductTypesLiterals]
    subscriptions: Optional[List[AccountSubscriptionTypesLiterals]]
    available_subscriptions: Optional[List[AccountSubscriptionTypesLiterals]]
    restricted_subscriptions: Optional[List[AccountSubscriptionTypesLiterals]]
    attribute: Optional[Union[str, AccountAttributes]]
    sensitive: Optional[Union[str, AccountSensitive]]
    balance: Optional[Union[str, AccountBalance]]
    card_brand: Optional[Union[str, AccountCardBrand]]
    payoff: Optional[Union[str, AccountPayoff]]
    transaction: Optional[Union[str, AccountTransaction]]
    payment_instrument: Optional[Union[str, AccountPaymentInstrument]]
    update: Optional[Union[str, AccountUpdate]]
    latest_verification_session: Optional[Union[str, AccountVerificationSession]]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str
    metadata: Optional[Dict[str, str]]


T = TypeVar('T', bound='Account')


class AccountWithdrawConsentOpts(TypedDict):
    type: Literal['withdraw']
    reason: Optional[Literal['holder_withdrew_consent']]


class AccountSubResources:
    balances: AccountBalancesResource
    card_brands: AccountCardBrandsResource
    payoffs: AccountPayoffsResource
    sensitive: AccountSensitiveResource
    subscriptions: AccountSubscriptionsResource
    transactions: AccountTransactionsResource
    updates: AccountUpdatesResource
    verification_sessions: AccountVerificationSessionResource
    products: AccountProductResource
    attributes: AccountAttributesResource
    payment_instruments: AccountPaymentInstrumentsResource

    def __init__(self, _id: str, config: Configuration):
        self.balances = AccountBalancesResource(config.add_path(_id))
        self.card_brands = AccountCardBrandsResource(config.add_path(_id))
        self.payoffs = AccountPayoffsResource(config.add_path(_id))
        self.sensitive = AccountSensitiveResource(config.add_path(_id))
        self.subscriptions = AccountSubscriptionsResource(config.add_path(_id))
        self.transactions = AccountTransactionsResource(config.add_path(_id))
        self.payment_instruments = AccountPaymentInstrumentsResource(config.add_path(_id))
        self.updates = AccountUpdatesResource(config.add_path(_id))
        self.verification_sessions = AccountVerificationSessionResource(config.add_path(_id))
        self.products = AccountProductResource(config.add_path(_id))
        self.attributes = AccountAttributesResource(config.add_path(_id))

class AccountResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountResource, self).__init__(config.add_path('accounts'))

    def __call__(self, acc_id: str) -> AccountSubResources:
        return AccountSubResources(acc_id, self.config)

    def retrieve(self, acc_id: str, params: Optional[Dict[str, List[AccountExpandableFieldsLiterals]]] = None) -> MethodResponse[Account]:
        return super(AccountResource, self)._get_with_sub_path_and_params(acc_id, params)

    def list(self, params: Optional[AccountListOpts[T]] = None) -> MethodResponse[List[Account]]:
        return super(AccountResource, self)._list(params)

    def create(self, opts: Union[AccountACHCreateOpts, AccountLiabilityCreateOpts], request_opts: Optional[RequestOpts] = None) -> MethodResponse[Account]:
        return super(AccountResource, self)._create(opts, request_opts)

    def withdraw_consent(self, acc_id: str, data: AccountWithdrawConsentOpts = { 'type': 'withdraw', 'reason': 'holder_withdrew_consent' }) -> MethodResponse[Account]: # pylint: disable=dangerous-default-value
        return super(AccountResource, self)._create_with_sub_path('{acc_id}/consent'.format(acc_id=acc_id), data)
