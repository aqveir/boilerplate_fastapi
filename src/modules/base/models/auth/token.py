from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, PositiveInt

class Token(BaseModel):
    access_token: str = None
    token_type: str = "bearer"
    refesh_token: str | None = None
    id_token: str | None = None
    created_at: PositiveInt = int(datetime.now(tz=timezone.utc).timestamp())
    expires_at: PositiveInt | None = None

    model_config = ConfigDict(extra='allow')