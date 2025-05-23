""" Import the required modules """
import datetime
from typing import Optional
from uuid import UUID

# Importing necessary modules from SQLAlchemy
from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Boolean,
    MetaData
)
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    DeclarativeBase, declarative_base,
    Mapped, mapped_column
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import AbstractConcreteBase


metadata_obj = MetaData()


class BaseDB(AsyncAttrs, DeclarativeBase):
    """
    Base class for all models.
    """
    metadata = metadata_obj


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
        sort_order=1000
    )
    created_by: Mapped[int] = mapped_column(
        BigInteger, default=0,
        sort_order=1001
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        onupdate=func.UTC_TIMESTAMP(),
        sort_order=1002
    )
    updated_by: Mapped[Optional[int]] = mapped_column(
        BigInteger, nullable=True,
        sort_order=1003
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=1,
        sort_order=1010
    )


class BaseSchemaUUID(AbstractBaseSchema):
    """
    Base schema for all models requiring UUID and audit logging.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Unique identifiers
    hash: Mapped[UUID] = mapped_column(
        String, unique=True, index=True,
        sort_order=-9
    )


class BaseSchemaAuditLogDeleteLog(BaseSchemaAuditLog):
    """
    Base schema for all models.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Audit fields (Delete log)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        sort_order=1004
    )
    deleted_by: Mapped[Optional[int]] = mapped_column(
        BigInteger, nullable=True,
        sort_order=1005
    )


class BaseSchemaUUIDAuditLogDeleteLog(
    BaseSchemaUUID, BaseSchemaAuditLogDeleteLog):
    """
    Base schema for all models requiring UUID and audit logging.
    This schema defines the structure of the base data.
    """
    pass

BaseSchema = declarative_base()
