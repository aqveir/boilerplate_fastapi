""" Import the required modules """
from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    Boolean,
    String,
)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)

# Import Base Schema classes & models
from modules.base.db.base import (
    BaseDB,
    BaseSchemaAuditLog
)
from modules.base.enums import DataType

if TYPE_CHECKING:
    from modules.core.schemas import (
        ConfigurationSchema,
        OrganizationSchema
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
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
    configuration_id: Mapped[int] = mapped_column(
        ForeignKey("configurations.id"), nullable=False
    )

    # Entity fields
    data_value: Mapped[str] = mapped_column(
        String(8000), nullable=False, index=True
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean, default=False,
        server_default="0"
    )

    # Relationships
    organization: Mapped["OrganizationSchema"] = relationship(
        "OrganizationSchema", back_populates="configurations"
    )
    configuration: Mapped["ConfigurationSchema"] = relationship(
        single_parent=True, uselist=False
    )
