"""REST client handling, including payspaceStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
from urllib.parse import urlsplit, parse_qsl

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator, OAuthAuthenticator

from tap_payspace.authenticator import OAuthPayspaceAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class payspaceStream(RESTStream):
    """payspace stream class."""

    records_jsonpath = "$.value[*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    @property
    def auth_url(self) -> str:
        """Return the Auth URL, configurable via tap settings."""
        return self.config["auth_url"]

    @property
    def company_id(self) -> str:
        return self.config["company_id"]

    @property
    def authenticator(self) -> OAuthAuthenticator:
        """Return a new authenticator object."""
        return OAuthPayspaceAuthenticator(
            self, self.auth_url, self.config["client_id"], self.config["client_secret"]
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        next_page_token = response.headers.get("odata.nextlink", None)

        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            query_string = urlsplit(next_page_token).query
            params.update(parse_qsl(query_string))
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.
        return row
