"""Add lookup data

Revision ID: 726c6c49b353
Revises: 7b2335731c2d
Create Date: 2025-05-25 16:40:17.413898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '726c6c49b353'
down_revision: Union[str, None] = '7b2335731c2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    lookup_table = sa.sql.table(
        'lookups',
        sa.sql.column('lookup_type', sa.String),
        sa.sql.column('lookup_key', sa.String),
        sa.sql.column('display_value', sa.String),
        sa.sql.column('description', sa.String),
        sa.sql.column('is_default', sa.Boolean),
        sa.sql.column('is_secure', sa.Boolean),
        sa.sql.column('order_by', sa.Integer),
    )
    op.bulk_insert(
        lookup_table,
        [
            # Add organization types
            {
                'lookup_type': 'organization_type',
                'lookup_key': 'organization_type_corporate',
                'display_value': 'Corporate',
                'description': 'Corporate, Business',
                'is_default': True,
                'is_secure': True,
                'order_by': 0
            },
            {
                'lookup_type': 'organization_type',
                'lookup_key': 'organization_type_reseller',
                'display_value': 'Reseller',
                'description': 'Reseller, Partner',
                'is_default': False,
                'is_secure': True,
                'order_by': 1
            },
            {
                'lookup_type': 'organization_type',
                'lookup_key': 'organization_type_internal',
                'display_value': 'Internal',
                'description': 'Internal, Employee',
                'is_default': False,
                'is_secure': True,
                'order_by': 2
            },
            {
                'lookup_type': 'organization_type',
                'lookup_key': 'organization_type_individual',
                'display_value': 'Individual',
                'description': 'Individual, Personal',
                'is_default': False,
                'is_secure': True,
                'order_by': 3
            },
            # Add organization industries types
            {
                'lookup_type': 'organization_industry',
                'lookup_key': 'organization_industry_default',
                'display_value': 'Default',
                'description': 'Default, Vanilla Industry',
                'is_default': True,
                'is_secure': True,
                'order_by': 0
            },
        ],
        multiinsert=False
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
