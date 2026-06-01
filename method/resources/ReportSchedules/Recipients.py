from typing import TypedDict, Optional, List

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.ReportSchedules.Types import ReportSchedule


class ReportScheduleRecipientAddOpts(TypedDict):
    recipient: str


class ReportScheduleRecipientsReplaceOpts(TypedDict):
    recipients: List[str]


class ReportScheduleRecipientsResource(Resource):
    def __init__(self, config: Configuration):
        super(ReportScheduleRecipientsResource, self).__init__(config.add_path('recipients'))

    def add(self, opts: ReportScheduleRecipientAddOpts) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleRecipientsResource, self)._create(opts)

    def replace(self, opts: ReportScheduleRecipientsReplaceOpts) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleRecipientsResource, self)._update(opts)

    def delete(self, recipient: Optional[str] = None) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleRecipientsResource, self)._delete_with_params({ 'recipient': recipient } if recipient else {})
