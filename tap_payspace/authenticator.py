from singer_sdk.authenticators import OAuthAuthenticator
from singer_sdk.streams import RESTStream

class OAuthPayspaceAuthenticator(OAuthAuthenticator):
    def __init__(
        self,
        stream: RESTStream,
        auth_endpoint: str,
        client_id: str,
        client_secret: str,
        oauth_scopes: str = "api.read_only",
        default_expiration: int = 3600,
    ) -> None:
        super().__init__(stream, auth_endpoint, oauth_scopes, default_expiration)
        self._client_id = client_id
        self._client_secret = client_secret


    @property
    def oauth_request_body(self) -> dict:
        if self.client_id == None or self.client_secret == None:
            raise ValueError(
                "Missing client_id and/or client_secret property for the OAuth payload"
            )
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.oauth_scopes or "api.read_only",
        }
