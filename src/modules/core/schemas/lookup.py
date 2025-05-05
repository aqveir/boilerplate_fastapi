""" Import the required modules """
from typing import Optional
from sqlalchemy import (
    Boolean,
    Integer,
    String,
    BigInteger
)
from sqlalchemy.orm import (Mapped, mapped_column)

# Import Base Schema classes & models
from modules.base.db.base import (
    BaseDB,
    BaseSchemaAuditLog
)

# Import Enums
from modules.core.enums.lookup import LookupMaster


class LookUpSchema(BaseSchemaAuditLog, BaseDB):
    """
    LookUp model for the application.
    This model defines the structure of the lookup data.
    The base schema is inherited from BaseSchema_UUID_AuditLog_DeleteLog.
    This schema defines the structure of the base data. This schema
    includes the following fields:
    - id: Unique identifier for the lookup.
    
    """
    __tablename__ = "lookups"

    # Foreign fields
    organization_id: Mapped[int] = mapped_column(
        BigInteger, default=0, index=True
    )

    # Entity fields
    lookup_type: Mapped[LookupMaster] = mapped_column(String(128), index=True)
    lookup_key: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    lookup_value: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(
        String(8000), nullable=True
    )

    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_secure: Mapped[bool] = mapped_column(Boolean, default=False)  # Not User Editable
    order_by: Mapped[int] = mapped_column(Integer, default=0)
