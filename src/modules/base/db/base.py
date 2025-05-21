""" Import the required modules """
import dataclasses
import datetime
from typing import Optional
from uuid import UUID

# Importing necessary modules from SQLAlchemy
from sqlalchemy import (
    BigInteger,
    String,
    Uuid,
    DateTime,
    Boolean
)
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    DeclarativeBase, declarative_base,
    Mapped, mapped_column
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import AbstractConcreteBase


@dataclasses.dataclass
class BaseDB(AsyncAttrs, DeclarativeBase):
    """
    Base class for all models.
    """
    pass


@dataclasses.dataclass
class AbstractBaseSchema(AbstractConcreteBase):
    """
    Base schema for all models.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Primary key and unique identifiers
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, index=True,
        autoincrement=True, sort_order=-10
    )


@dataclasses.dataclass
class BaseSchemaAuditLog(AbstractBaseSchema):
    """
    Base schema for all models requiring audit logging.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Audit fields
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.UTC_TIMESTAMP(),
        sort_order=100
    )
    created_by: Mapped[int] = mapped_column(
        BigInteger, default=0, sort_order=101
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        onupdate=func.UTC_TIMESTAMP(), sort_order=102
    )
    updated_by: Mapped[Optional[int]] = mapped_column(
        BigInteger, nullable=True, sort_order=103
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=1, sort_order=110
    )


@dataclasses.dataclass
class BaseSchemaUUID(AbstractBaseSchema):
    """
    Base schema for all models requiring UUID and audit logging.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Unique identifiers
    hash: Mapped[str] = mapped_column(
        String, unique=True, index=True,
        sort_order=-9
    )


@dataclasses.dataclass
class BaseSchemaAuditLogDeleteLog(BaseSchemaAuditLog):
    """
    Base schema for all models.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Audit fields (Delete log)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        sort_order=104
    )
    deleted_by: Mapped[Optional[int]] = mapped_column(
        BigInteger, nullable=True,
        sort_order=105
    )


@dataclasses.dataclass
class BaseSchemaUUIDAuditLogDeleteLog(BaseSchemaUUID, BaseSchemaAuditLogDeleteLog):
    """
    Base schema for all models requiring UUID and audit logging.
    This schema defines the structure of the base data.
    """
    pass

BaseSchema = declarative_base()
