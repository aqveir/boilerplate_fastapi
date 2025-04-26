""" Import the python standard libraries """
from pydantic import Field

# Import the project models
from modules.base.models.base import AppBaseModelWithAuditLog

# Import the enums
from modules.core.enums.lookup import LookupMaster


class Lookup(AppBaseModelWithAuditLog):
    """
    Lookup model for the application.
    """
    key: str = Field(default=None, description="Name",
        exclude=True, max_length=128, examples=["my_lookup"])
    display_value: str = Field(default=None, description="Value",
        exclude=True, max_length=128, examples=["My Lookup Value"])
    description: str = Field(default=None, description="Description",
        exclude=True, max_length=256, examples=["My Lookup Description"])

    lookup_type: LookupMaster = Field(default=None,
        description="Lookup Type", exclude=True,
        examples=["organization_type"])

    order_by: int = Field(default=0, description="Order By",
        exclude=True, examples=[1])
    is_editable: bool = Field(default=True, description="Is Editable",
        exclude=True, examples=[True])
