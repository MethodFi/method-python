from typing import TypedDict, List

from method.resource import MethodResponse, Resource
from method.configuration import Configuration
from method.resources.Report import ReportTypesLiterals
from method.resources.ReportSchedules.Types import ReportSchedule


class ReportScheduleTypeAddOpts(TypedDict):
    type: ReportTypesLiterals


class ReportScheduleTypesReplaceOpts(TypedDict):
    types: List[ReportTypesLiterals]


class ReportScheduleTypesResource(Resource):
    def __init__(self, config: Configuration):
        super(ReportScheduleTypesResource, self).__init__(config.add_path('types'))

    def add(self, opts: ReportScheduleTypeAddOpts) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleTypesResource, self)._create(opts)

    def replace(self, opts: ReportScheduleTypesReplaceOpts) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleTypesResource, self)._update(opts)

    def delete(self, report_type: ReportTypesLiterals) -> MethodResponse[ReportSchedule]:
        return super(ReportScheduleTypesResource, self)._delete_with_params({ 'type': report_type })
