"""add user email verification timestamp

Revision ID: e4a1b0c2d3e4
Revises: f0bd01a18a3d
Create Date: 2026-09-22
"""

from collections.abc import Sequence
import time

import sqlalchemy as sa
from alembic import context, op


revision: str = 'e4a1b0c2d3e4'
down_revision: str | None = 'f0bd01a18a3d'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _has_column() -> bool:
    return 'email_verified_at' in {column['name'] for column in sa.inspect(op.get_bind()).get_columns('user')}


def upgrade() -> None:
    if context.is_offline_mode():
        op.add_column('user', sa.Column('email_verified_at', sa.BigInteger(), nullable=True))
    elif not _has_column():
        op.add_column('user', sa.Column('email_verified_at', sa.BigInteger(), nullable=True))

    # Existing accounts predate verification and must retain their access.
    migration_timestamp = int(time.time())
    op.execute(
        sa.text('UPDATE "user" SET email_verified_at = :timestamp WHERE email_verified_at IS NULL').bindparams(
            timestamp=migration_timestamp
        )
    )


def downgrade() -> None:
    if context.is_offline_mode() or _has_column():
        op.drop_column('user', 'email_verified_at')
