import datetime
from typing import List

# Importing necessary modules from SQLAlchemy
from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
    DateTime,
    Boolean,
    String
)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)

# Import Base Schema classes & models
from modules.base.db.base import *
from .lookup import LookUp
from .organization_configuration import Organization_Configuration

# Importing 

class Organization(BaseSchema_UUID_AuditLog_DeleteLog):
    """
    Organization model for the application.
    This model defines the structure of the organization data.

    The base schema is inherited from BaseSchema_UUID_AuditLog_DeleteLog.
    This schema defines the structure of the base data. This schema
    includes the following fields:
    - id: Unique identifier for the organization.
    - hash: UUID for the organization.
    
    """
    __tablename__ = "organizations"

    # Foreign fields
    type_id: Mapped[int] = mapped_column(ForeignKey("lookup.id"))

    # Entity fields
    display_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    legal_name: Mapped[str] = mapped_column(String(128), nullable=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    logo: Mapped[str] = mapped_column(String(256), nullable=True)

    # Domain fields
    subdomain: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    custom_domain: Mapped[str] = mapped_column(String(128), nullable=True, index=True)

    # Address fields
    address: Mapped[str] = mapped_column(String(256), nullable=True)
    locality: Mapped[str] = mapped_column(String(256), nullable=True)
    city: Mapped[str] = mapped_column(String(128), nullable=True)
    state_id: Mapped[int] = mapped_column(Integer, nullable=True)
    country_id: Mapped[int] = mapped_column(Integer, nullable=True)
    zipcode: Mapped[str] = mapped_column(String(32), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    # Contact fields
    phone: Mapped[str] = mapped_column(String(32), nullable=True, index=True)
    email: Mapped[str] = mapped_column(String(128), nullable=True, index=True)

    # Extra fields
    search_tags: Mapped[str] = mapped_column(String(256), nullable=True, index=True)
    website: Mapped[str] = mapped_column(String(256), nullable=True)

    # External Payment fields (e.g. Stripe)
    payment_provider: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    payment_provider_customer_id: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    trial_ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, index=True)

    # Relationships
    type: Mapped["LookUp"] = relationship("LookUp", back_populates="organizations")
    configurations: Mapped[List["Organization_Configuration"]] = relationship(back_populates="organizations")
    