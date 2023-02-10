"""Stream type classes for tap-payspace."""

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_payspace.client import payspaceStream

class EmployeesStream(payspaceStream):
    """TODO: Docs."""

    @property
    def path(self) -> str:
        return f"/odata/v1.1/{self.company_id}/Employee"

    name = "employees"
    primary_keys = ["EmployeeNumber"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("EmployeeNumber", th.StringType),
        th.Property("Title", th.StringType),
        th.Property("FirstName", th.StringType),
        th.Property("LastName", th.StringType),
        th.Property("PreferredName", th.StringType),
        th.Property("Email", th.StringType),
        th.Property("Birthday", th.DateTimeType),
        th.Property("DateCreated", th.DateTimeType),
        th.Property("IsRetired", th.BooleanType),
    ).to_dict()

class LeaveApplicationsStream(payspaceStream):
    """TODO: Docs"""

    @property
    def path(self) -> str:
        return f"/odata/v1.1/{self.company_id}/EmployeeLeaveApplication"

    name = "leave_applications"
    primary_keys = ["LeaveAdjustmentId"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("LeaveAdjustmentId", th.IntegerType),
        th.Property("EmployeeNumber", th.StringType),
        th.Property("FullName", th.StringType),
        th.Property("LeaveType", th.StringType),
        th.Property("LeaveCompanyRun", th.StringType),
        th.Property("NoOfDays", th.NumberType),
        th.Property("LeaveStartDate", th.DateTimeType),
        th.Property("LeaveEndDate", th.DateTimeType),
        th.Property("LeaveStatus", th.StringType),
    ).to_dict()
