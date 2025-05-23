""" Import the required modules """
from typing import Optional
from sqlalchemy import (
    Boolean,
    String,
    Text,
)
from sqlalchemy.orm import (Mapped, mapped_column)

# Import Base Schema classes & models
from modules.base.db.base import (
    BaseDB,
    BaseSchemaAuditLog
)
from modules.base.enums import DataType


class ConfigurationSchema(BaseSchemaAuditLog, BaseDB):
    """
    Conguturation meta data model for the organization.
    This model defines the structure of the configuration data.

    The base schema is referenced into the organization configuration
    schema.
    """
    __tablename__ = "configurations"

    # Entity fields
    data_type: Mapped[DataType] = mapped_column(
        String(64), nullable=False,
        server_default=DataType.STRING.value,
        index=True
    )
    data_key: Mapped[str] = mapped_column(
        String(128), nullable=False,
        index=True
    )
    display_name: Mapped[Optional[str]] = mapped_column(
        String(256), nullable=True,
        index=False
    )    
    data_schema: Mapped[str] = mapped_column(
        Text(256), nullable=True,
        index=False
    )
    default_value: Mapped[str] = mapped_column(
        Text(256), nullable=True,
        index=False
    )
    filter: Mapped[str] = mapped_column(
        String(128), nullable=True,
        index=False
    )

    allow_multiple: Mapped[bool] = mapped_column(
        Boolean, default=False,
        server_default="0",
        comment="Mark true if multiple values are allowed",
        index=False
    )

    is_secure: Mapped[bool] = mapped_column(
        Boolean, default=False,
        comment="This field is not user editable",
        server_default="0",
        index=False
    )
