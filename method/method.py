from method.configuration import Configuration, ConfigurationOpts
from method.resources.Account import AccountResource
from method.resources.Bin import BinResource
from method.resources.Entity import EntityResource
from method.resources.Element import ElementResource
from method.resources.Merchant import MerchantResource
from method.resources.Payment import PaymentResource
from method.resources.Report import ReportResource
from method.resources.RoutingNumber import RoutingNumberResource
from method.resources.Webhook import WebhookResource
from method.resources.HealthCheck import PingResponse, HealthCheckResource


class Method:
    accounts: AccountResource
    bins: BinResource
    entities: EntityResource
    elements: ElementResource
    merchants: MerchantResource
    payments: PaymentResource
    reports: ReportResource
    routing_numbers: RoutingNumberResource
    webhooks: WebhookResource
    healthcheck: HealthCheckResource

    def __init__(self, opts: ConfigurationOpts = None, **kwargs: ConfigurationOpts):
        _opts: ConfigurationOpts = {**(opts or {}), **kwargs}  # type: ignore
        config = Configuration(_opts)

        self.accounts = AccountResource(config)
        self.bins = BinResource(config)
        self.entities = EntityResource(config)
        self.elements = ElementResource(config)
        self.merchants = MerchantResource(config)
        self.payments = PaymentResource(config)
        self.reports = ReportResource(config)
        self.routing_numbers = RoutingNumberResource(config)
        self.webhooks = WebhookResource(config)
        self.healthcheck = HealthCheckResource(config)

    def ping(self) -> PingResponse:
        return self.healthcheck.get()
