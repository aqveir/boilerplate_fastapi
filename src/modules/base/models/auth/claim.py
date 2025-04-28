from pydantic import BaseModel, ConfigDict, UUID1, computed_field

from .token import Token as AuthToken


class AuthClaim(BaseModel):
    """
    AuthClaim model for the application.
    This model is used to store the authentication claim for a user.
    It contains the token, user data, privileges, settings, and unread notifications.
    """
    token: AuthToken | None = None
    user: dict = {}
    privileges: list = []
    settings: list = []
    unread_notifications: int = 0

    @computed_field(description="Claim ID")
    @property
    def key(self) -> str | None:
        if self.token is None:
            return None
        return self.token.access_token


    @computed_field(description="Claim TTL")
    @property
    def ttl(self) -> int:
        if self.token is None:
            return None
        return self.token.expires_at


    model_config = ConfigDict(
        extra='allow', populate_by_name=True, 
        from_attributes=True
    )
