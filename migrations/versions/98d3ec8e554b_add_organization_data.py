"""Add organization data

Revision ID: 98d3ec8e554b
Revises: 8547ccfb65df
Create Date: 2025-05-25 15:27:41.453440

"""
from typing import List, Sequence, Union

from alembic import op
import sqlalchemy as sa

from modules.base.config import config


# revision identifiers, used by Alembic.
revision: str = '98d3ec8e554b'
down_revision: Union[str, None] = '8547ccfb65df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    organization_table = sa.sql.table(
        'organizations',
        sa.sql.column('type_id', sa.BigInteger),
        sa.sql.column('display_name', sa.String),
        sa.sql.column('legal_name', sa.String),
        sa.sql.column('subdomain', sa.String),
    )

    # Geenrate initial organization data
    organization_data: List[dict[str, str]] = list()
    organization_data.append({
        'type_id': 1,
        'display_name': 'EllaiSys',
        'legal_name': 'Ellai Information Systems Pvt. Ltd.',
        'subdomain': 'ellaisys'
    })
    organization_data.append({
        'type_id': 1,
        'display_name': 'Demo Organization',
        'legal_name': 'Demo Organization Inc.',
        'subdomain': 'demo'
    })
    if config.ENVIRONMENT != 'development':
        for i in range(100):
            organization_data.append({
                'type_id': 1,
                'display_name': f'My Organization {i}',
                'legal_name': f'My Organization Inc. {i}',
                'subdomain': f'myorganization{i}'
            })

    op.bulk_insert(
        organization_table,
        organization_data,
        multiinsert=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
