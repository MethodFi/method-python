from method.configuration import Configuration, ConfigurationOpts
from method.resource import MethodResponse
from method.resources.Accounts import AccountResource
from method.resources.Entities import EntityResource
from method.resources.Elements import ElementResource
from method.resources.Merchant import MerchantResource
from method.resources.Payments import PaymentResource
from method.resources.Report import ReportResource
from method.resources.Webhook import WebhookResource
from method.resources.HealthCheck import PingResponse, HealthCheckResource
from method.resources.Simulate import SimulateResource


class Method:
    accounts: AccountResource
    entities: EntityResource
    elements: ElementResource
    merchants: MerchantResource
    payments: PaymentResource
    reports: ReportResource
    webhooks: WebhookResource
    healthcheck: HealthCheckResource
    simulate: SimulateResource

    def __init__(self, opts: ConfigurationOpts = None, **kwargs: ConfigurationOpts):
        _opts: ConfigurationOpts = {**(opts or {}), **kwargs}  # type: ignore
        config = Configuration(_opts)

        self.accounts = AccountResource(config)
        self.entities = EntityResource(config)
        self.elements = ElementResource(config)
        self.merchants = MerchantResource(config)
        self.payments = PaymentResource(config)
        self.reports = ReportResource(config)
        self.webhooks = WebhookResource(config)
        self.healthcheck = HealthCheckResource(config)
        self.simulate = SimulateResource(config)

    def ping(self) -> MethodResponse[PingResponse]:
        return self.healthcheck.retrieve()
