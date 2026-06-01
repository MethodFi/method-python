from typing import TypedDict, List

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.ReportSchedules.Types import ReportSchedule, ReportScheduleDeliveryMethodsLiterals


class ReportScheduleDeliveryMethodAddOpts(TypedDict):
    delivery_method: ReportScheduleDeliveryMethodsLiterals


class ReportScheduleDeliveryMethodsReplaceOpts(TypedDict):
    delivery_methods: List[ReportScheduleDeliveryMethodsLiterals]


class ReportScheduleDeliveryMethodsResource(Resource):
    def __init__(self, config: Configuration):
        super(ReportScheduleDeliveryMethodsResource, self).__init__(config.add_path('delivery_methods'))

    def add(self, opts: ReportScheduleDeliveryMethodAddOpts) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleDeliveryMethodsResource, self)._create(opts)

    def replace(self, opts: ReportScheduleDeliveryMethodsReplaceOpts) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleDeliveryMethodsResource, self)._update(opts)

    def delete(self, delivery_method: ReportScheduleDeliveryMethodsLiterals) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleDeliveryMethodsResource, self)._delete_with_params({ 'delivery_method': delivery_method })
