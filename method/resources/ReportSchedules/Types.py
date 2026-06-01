from typing import TypedDict, Optional, List, Literal

from method.resources.Report import ReportTypesLiterals


ReportScheduleStatusesLiterals = Literal[
    'active',
    'inactive'
]


ReportScheduleDeliveryMethodsLiterals = Literal[
    'webhook',
    'email'
]


class ReportSchedule(TypedDict):
    id: str
    types: List[ReportTypesLiterals]
    delivery_methods: List[ReportScheduleDeliveryMethodsLiterals]
    recipients: Optional[List[str]]
    cron: str
    status: ReportScheduleStatusesLiterals
    created_at: str
    updated_at: str


class ReportScheduleCreateOpts(TypedDict):
    types: List[ReportTypesLiterals]
    delivery_methods: List[ReportScheduleDeliveryMethodsLiterals]
    recipients: Optional[List[str]]
    cron: Optional[str]


class ReportScheduleUpdateOpts(TypedDict):
    cron: str
