"""Add organization data

Revision ID: 98d3ec8e554b
Revises: 8547ccfb65df
Create Date: 2025-05-25 15:27:41.453440

"""
import faker
import random
from typing import List, Sequence, Union

from alembic import op
import sqlalchemy as sa

from modules.base.config import config


# revision identifiers, used by Alembic.
revision: str = '98d3ec8e554b'
down_revision: Union[str, None] = '8547ccfb65df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Initialize Faker instance
fake = faker.Faker()

def upgrade() -> None:
    """Upgrade schema."""
    organization_table = sa.sql.table(
        'organizations',
        sa.sql.column('type_id', sa.BigInteger),
        sa.sql.column('display_name', sa.String),
        sa.sql.column('legal_name', sa.String),
        sa.sql.column('subdomain', sa.String),
        sa.sql.column('custom_domain', sa.String),
        sa.sql.column('address', sa.String),
        sa.sql.column('locality', sa.String),
        sa.sql.column('city', sa.String),
        sa.sql.column('zipcode', sa.String),
        sa.sql.column('latitude', sa.Double),
        sa.sql.column('longitude', sa.Double),
        sa.sql.column('phone', sa.String),
        sa.sql.column('email', sa.String),
        sa.sql.column('payment_provider', sa.String),
    )

    # Geenrate initial organization data
    organization_data: List[dict[str, str]] = list()
    organization_data.append({
        'type_id': 1,
        'display_name': 'EllaiSys',
        'legal_name': 'Ellai Information Systems Pvt. Ltd.',
        'subdomain': 'ellaisys',
        'custom_domain': 'ellaisys.com',
        'address': '1234 Elm Street',
        'locality': 'Tech City',
        'city': 'Innovation Hub',
        'phone': '+1-234-567-8900',
        'email': 'ellaisys@gmail.com',
        'payment_provider': 'stripe'
    })
    organization_data.append({
        'type_id': 1,
        'display_name': 'Demo Organization',
        'legal_name': 'Demo Organization Inc.',
        'subdomain': 'demo',
        'custom_domain': 'demo.com',
        'address': '5678 Oak Avenue',
        'locality': 'Sample Town',
        'city': 'Example City',
        'phone': '+1-987-654-3210',
        'email': 'ellaisys+demo@gmail.com',
        'payment_provider': 'stripe'
    })
    if config.ENVIRONMENT != 'development':
        for i in range(100):
            organization_data.append({
                'type_id': 1,
                'display_name': fake.company(),
                'legal_name': fake.company(),
                'subdomain': fake.domain_name().split('.')[0],
                'custom_domain': fake.domain_name(),
                'address': fake.street_address(),
                'locality': fake.street_name(),
                'city': fake.city(),
                'zipcode': fake.postcode(),
                'latitude': random.uniform(20, 50),
                'longitude': random.uniform(-130, -70),
                'phone': fake.phone_number(),
                'email': fake.email(),
                'payment_provider': fake.random_element(elements=('stripe', 'paypal', 'razorpay', 'square'))
            })

    op.bulk_insert(
        organization_table,
        organization_data,
        multiinsert=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
