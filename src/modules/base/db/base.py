from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column)
from sqlalchemy import (
    Column,
    Integer,
    UUID,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
)


class BaseDB(DeclarativeBase):
    pass


class BaseSchema(BaseDB):
    """
    Base schema for all models.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Primary key and unique identifiers
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)


class BaseSchema_AuditLog(BaseSchema):
    """
    Base schema for all models requiring audit logging.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Audit fields
    created_at = Column(DateTime, default=DateTime.utcnow())
    created_by = Column(Integer, default=0)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(Integer, nullable=True)
    is_active = Column(Integer, default=1)


class BaseSchema_UUID_AuditLog(BaseSchema):
    """
    Base schema for all models requiring UUID and audit logging.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Unique identifiers
    hash: Mapped[UUID] = Column(UUID, unique=True, index=True)

    # Audit fields
    created_at = Column(DateTime, default=DateTime.utcnow())
    created_by = Column(Integer, default=0)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_active = Column(Integer, default=1)


class BaseSchema_UUID_AuditLog_DeleteLog(BaseSchema_UUID_AuditLog):
    """
    Base schema for all models.
    This schema defines the structure of the base data.
    """
    __abstract__ = True

    # Audit fields (Delete log)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(Integer, nullable=True)