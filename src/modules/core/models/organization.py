from typing import Annotated, Self


from pydantic import ConfigDict, Field

# Import the project models
from modules.base.models.base import AppBaseModelWithHashAndAuditLog

class Organization(AppBaseModelWithHashAndAuditLog):
    """
    Organization model for the application.
    """

    display_name: str = Field(default=None, description="Display Name", max_length=128, examples=["My Organization"])
    legal_name: str = Field(default=None, description="Legal Name", exclude=True, max_length=129, examples=["My Organization Inc"])

    model_config = ConfigDict(
        extra='forbid', 
        populate_by_name=True, 
        from_attributes=True
    )