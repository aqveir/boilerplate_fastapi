""" Import the required modules """
from typing import Optional, TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    Boolean,
    String,
    Text,
)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)

# Import Base Schema classes & models
from modules.base.db.base import (
    BaseDB,
    BaseSchemaAuditLog
)
from modules.base.enums import DataType

if TYPE_CHECKING:
    #from modules.core.schemas.lookup import LookUp

    from modules.core.schemas import (
        OrganizationSchema as Organization
    )


class OrganizationConfigurationSchema(BaseSchemaAuditLog, BaseDB):
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
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

    # Entity fields
    data_type: Mapped[DataType] = mapped_column(
        String(64), nullable=False, index=True
    )
    data_key: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True
    )
    data_value: Mapped[str] = mapped_column(
        Text, nullable=False, index=True
    )
    display_name: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )

    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_secure: Mapped[bool] = mapped_column(Boolean, default=False) #Not User Editable

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="organization_configurations"
    )
