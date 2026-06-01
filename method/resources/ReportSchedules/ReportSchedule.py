from typing import Optional, List

from method.resource import MethodResponse, Resource, RequestOpts
from method.configuration import Configuration
from method.resources.ReportSchedules.Types import (
    ReportSchedule,
    ReportScheduleCreateOpts,
    ReportScheduleUpdateOpts,
)
from method.resources.ReportSchedules.ReportTypes import ReportScheduleTypesResource
from method.resources.ReportSchedules.DeliveryMethods import ReportScheduleDeliveryMethodsResource
from method.resources.ReportSchedules.Recipients import ReportScheduleRecipientsResource


class ReportScheduleSubResources:
    types: ReportScheduleTypesResource
    delivery_methods: ReportScheduleDeliveryMethodsResource
    recipients: ReportScheduleRecipientsResource

    def __init__(self, _id: str, config: Configuration):
        self.types = ReportScheduleTypesResource(config.add_path(_id))
        self.delivery_methods = ReportScheduleDeliveryMethodsResource(config.add_path(_id))
        self.recipients = ReportScheduleRecipientsResource(config.add_path(_id))


class ReportScheduleResource(Resource):
    def __init__(self, config: Configuration):
        super(ReportScheduleResource, self).__init__(config.add_path('report_schedules'))

    def __call__(self, rpt_sch_id: str) -> ReportScheduleSubResources:
        return ReportScheduleSubResources(rpt_sch_id, self.config)

    def retrieve(self, rpt_sch_id: str) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleResource, self)._get_with_id(rpt_sch_id)

    def list(self) -> MethodResponse[List[ReportSchedule]]:
        return super(ReportScheduleResource, self)._list()

    def create(self, opts: ReportScheduleCreateOpts, request_opts: Optional[RequestOpts] = None) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleResource, self)._create(opts, request_opts)

    def update(self, rpt_sch_id: str, opts: ReportScheduleUpdateOpts) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleResource, self)._patch_with_id(rpt_sch_id, opts)

    def delete(self, rpt_sch_id: str) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleResource, self)._delete(rpt_sch_id)
