"""payspace tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_payspace.streams import (
    EmployeesStream,
    LeaveApplicationsStream,
)

STREAM_TYPES = [
    EmployeesStream,
    LeaveApplicationsStream
]


class Tappayspace(Tap):
    """payspace tap class."""
    name = "tap-payspace"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            description="The client id for OAuth authentication",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.payspace.com",
            description="The url for the API service"
        ),
        th.Property(
            "auth_url",
            th.StringType,
            default="https://identity.yourhcm.com/connect/token",
            description="The url for the API service"
        ),
        th.Property(
            "company_id",
            th.StringType,
            required=True,
            description="The payspace company id to use"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    Tappayspace.cli()
