# Importing necessary modules from SQLAlchemy
from sqlalchemy import (
    ForeignKey,
    Boolean,
    String,
)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)

# Import Base Schema classes & models
from modules.base.db.base import *
from .organization import Organization

class Organization_Configuration(BaseSchema_AuditLog):
    """
    Organization Configuration model for the application.
    This model defines the structure of the organization configuration data.
    The base schema is inherited from BaseSchema_UUID_AuditLog_DeleteLog.
    This schema defines the structure of the base data. This schema
    includes the following fields:
    - id: Unique identifier for the organization configuration.
    
    """
    __tablename__ = "organization_configurations"

    # Foreign fields
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))

    # Entity fields
    data_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    data_key: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    data_value: Mapped[str] = mapped_column(String(8000), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(128), nullable=True)
    
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_secure: Mapped[bool] = mapped_column(Boolean, default=False) #Not User Editable

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="organization_configurations")