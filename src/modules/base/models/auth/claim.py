from pydantic import BaseModel, ConfigDict, UUID1, computed_field

from .token import Token as AuthToken


class AuthClaim(BaseModel):
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
    

    @computed_field(description="Claim User UUID")
    @property
    def hash(self) -> UUID1 | None:
        if self.user is None:
            return None
        return self.user.get('hash', None)
    

    @computed_field(description="Full name")
    @property
    def full_name(self) -> str | None:
        if self.user is None:
            return None
        return self.user.get('full_name', None)


    @computed_field
    @property
    def organization(self) -> dict | None:
        organization: dict = self.user.get('organization', None)
        print(organization)
        if organization is None:
            return None
        return organization


    model_config = ConfigDict(extra='allow', populate_by_name=True, from_attributes=True)
