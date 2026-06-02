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
from method.resources.Events import EventResource
from method.resources.CardProduct import CardProductResource
from method.resources.Opal import OpalResource
from method.resources.ForwardingRequests.ForwardingRequest import ForwardingRequestResource
from method.resources.Secrets.Secret import SecretResource
from method.resources.Teams.Team import TeamResource
from method.resources.ManagedAccounts.ManagedAccount import ManagedAccountResource

class Method:
    accounts: AccountResource
    entities: EntityResource
    elements: ElementResource
    events: EventResource
    merchants: MerchantResource
    payments: PaymentResource
    reports: ReportResource
    webhooks: WebhookResource
    healthcheck: HealthCheckResource
    simulate: SimulateResource
    card_products: CardProductResource
    opal: OpalResource
    forwarding_requests: ForwardingRequestResource
    secrets: SecretResource
    teams: TeamResource
    managed_accounts: ManagedAccountResource

    def __init__(self, opts: ConfigurationOpts = None, **kwargs: ConfigurationOpts):
        _opts: ConfigurationOpts = {**(opts or {}), **kwargs}  # type: ignore
        config = Configuration(_opts)

        self.accounts = AccountResource(config)
        self.entities = EntityResource(config)
        self.elements = ElementResource(config)
        self.events = EventResource(config)
        self.merchants = MerchantResource(config)
        self.payments = PaymentResource(config)
        self.reports = ReportResource(config)
        self.webhooks = WebhookResource(config)
        self.healthcheck = HealthCheckResource(config)
        self.simulate = SimulateResource(config)
        self.card_products = CardProductResource(config)
        self.opal = OpalResource(config)
        self.forwarding_requests = ForwardingRequestResource(config)
        self.secrets = SecretResource(config)
        self.teams = TeamResource(config)
        self.managed_accounts = ManagedAccountResource(config)
        
    def ping(self) -> MethodResponse[PingResponse]:
        return self.healthcheck.retrieve()
