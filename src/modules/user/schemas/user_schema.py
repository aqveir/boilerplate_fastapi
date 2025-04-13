from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import (relationship, Mapped, mapped_column)

from modules.base.db.base import *

class User(BaseSchema_UUID_AuditLog_DeleteLog):
    """
    User schema for serialization and validation.
    This schema defines the structure of the user data.
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    # User information
    title = Column(String, nullable=True)
    first_name = Column(String(64), nullable=True)
    middle_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)

    # User details
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)

    # Auth information
    username = Column(String(64), unique=True, index=True)

    email = Column(String(64), unique=True, index=True)

    # Relationships
    details: Mapped["UserDetail"] = relationship(
        "UserDetail", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class UserDetail(BaseSchema_UUID_AuditLog):
    """
    User details schema for serialization and validation.
    This schema defines the structure of the user details data.
    """
    __tablename__ = 'user_details'
    __table_args__ = {'extend_existing': True}

    # User information
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    address = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    profile_picture = Column(String(255), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="details", uselist=False, cascade="all, delete-orphan"
    )


    def __repr__(self):
        return f"<UserDetails(user_id={self.user_id}, address={self.address})>"


class UserAddress(BaseSchema_UUID_AuditLog):
    """
    User address schema for serialization and validation.
    This schema defines the structure of the user address data.
    """
    __tablename__ = 'user_addresses'
    __table_args__ = {'extend_existing': True}

    # User information
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    address_line_1 = Column(String(255), nullable=True)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="details", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<UserAddress(user_id={self.user_id}, address_line_1={self.address_line_1})>"


class UserStatus(BaseSchema_UUID_AuditLog):
    """
    User status schema for serialization and validation.
    This schema defines the structure of the user status data.
    """
    __tablename__ = 'user_statuses'
    __table_args__ = {'extend_existing': True}

    # User information
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"<UserStatus(user_id={self.user_id}, is_active={self.is_active})>"