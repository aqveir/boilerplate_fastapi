from pydantic import Field

# Import the project models
from modules.base.models.base import AppBaseModelWithHashAndAuditLog

# Define the Enum
class LookupMaster(str):
    """
    Lookup Master Type Enum.
    """
    ORGANIZATION_TYPE = "organization_type"
    USER_TYPE = "user_type"
    USER_STATUS = "user_status"



class Lookup(AppBaseModelWithHashAndAuditLog):
    """
    Lookup model for the application.
    """
    key: str = Field(default=None, description="Name", exclude=True, max_length=128, examples=["my_lookup"])
    display_value: str = Field(default=None, description="Value", exclude=True, max_length=128, examples=["My Lookup Value"])
    description: str = Field(default=None, description="Description", exclude=True, max_length=256, examples=["My Lookup Description"])

    lookup_type: LookupMaster = Field(default=None, description="Lookup Type", exclude=True, examples=["organization_type"])