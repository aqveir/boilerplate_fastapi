""" Import the required modules """
import datetime
from typing import List, Optional, TYPE_CHECKING

# Importing necessary modules from SQLAlchemy
from sqlalchemy import (
    Double,
    ForeignKey,
    Integer,
    DateTime,
    String
)
from sqlalchemy.orm import (Mapped, mapped_column, relationship)

# Import Base Schema classes & models
from modules.base.db.base import (
    BaseDB,
    BaseSchemaUUIDAuditLogDeleteLog
)

if TYPE_CHECKING:
    from modules.core.schemas import (
        LookUpSchema,
        OrganizationConfigurationSchema
    )


class OrganizationSchema(BaseSchemaUUIDAuditLogDeleteLog, BaseDB):
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
    type_id: Mapped[int] = mapped_column(ForeignKey("lookups.id"))

    # Entity fields
    display_name: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True
    )
    legal_name: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    logo: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    # Domain fields
    subdomain: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, index=True
    )
    custom_domain: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, index=True
    )

    # Address fields
    address: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    locality: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    state_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    country_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    zipcode: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    latitude: Mapped[float] = mapped_column(Double, nullable=True)
    longitude: Mapped[float] = mapped_column(Double, nullable=True)

    # Contact fields
    phone: Mapped[str] = mapped_column(String(32), nullable=True, index=False)
    email: Mapped[str] = mapped_column(String(128), nullable=True, index=False)

    # Extra fields
    search_tags: Mapped[Optional[str]] = mapped_column(
        String(256), nullable=True, index=False
    )
    website: Mapped[Optional[str]] = mapped_column(
        String(256), nullable=True
    )

    # External Payment fields (e.g. Stripe)
    payment_provider: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, index=False
    )
    payment_provider_customer_id: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, index=False
    )
    trial_ends_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True, index=False
    )

    # Relationships
    type: Mapped["LookUpSchema"] = relationship(
        single_parent=True, uselist=False
    )
    configurations: Mapped[List["OrganizationConfigurationSchema"]] = relationship(
        back_populates="organization"
    )
