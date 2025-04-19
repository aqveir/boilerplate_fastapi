from datetime import datetime
from uuid import UUID

# Importing necessary modules from SQLAlchemy
from sqlalchemy import (
    BigInteger,
    Uuid,
    DateTime,
    Boolean
)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column)


class BaseDB(DeclarativeBase):
    pass


class BaseSchema(BaseDB):
    """
    Base schema for all models.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Primary key and unique identifiers
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True, sort_order=-10)


class BaseSchema_AuditLog(BaseSchema):
    """
    Base schema for all models requiring audit logging.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=DateTime.utcnow(), sort_order=100)
    created_by: Mapped[int] = mapped_column(BigInteger, default=0, sort_order=101)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=DateTime.utcnow(), sort_order=102)
    updated_by: Mapped[int] = mapped_column(BigInteger, nullable=True, sort_order=103)
    is_active: Mapped[bool] = mapped_column(Boolean, default=1, sort_order=110)


class BaseSchema_UUID(BaseSchema):
    """
    Base schema for all models requiring UUID and audit logging.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Unique identifiers
    hash: Mapped[UUID] = mapped_column(Uuid, unique=True, index=True, sort_order=-9)


class BaseSchema_AuditLog_DeleteLog(BaseSchema_AuditLog):
    """
    Base schema for all models.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Audit fields (Delete log)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, sort_order=104)
    deleted_by: Mapped[int] = mapped_column(BigInteger, nullable=True, sort_order=105)


class BaseSchema_UUID_AuditLog_DeleteLog(BaseSchema_UUID, BaseSchema_AuditLog_DeleteLog):
    pass