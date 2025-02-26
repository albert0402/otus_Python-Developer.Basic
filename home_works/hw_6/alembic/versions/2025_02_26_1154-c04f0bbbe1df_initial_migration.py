"""Initial migration

Revision ID: c04f0bbbe1df
Revises:
Create Date: 2025-02-26 11:54:36.812504

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers, used by Alembic.
revision: str = "c04f0bbbe1df"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Enable citext extension if it is not already enabled
    op.execute("CREATE EXTENSION IF NOT EXISTS citext;")
    
    # Create the "tag" table
    op.create_table(
        "tag",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", postgresql.CITEXT(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("name", name=op.f("uq_tag_name")),
    )
    
    # Create the "users" table
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("username", sa.String(length=250), nullable=False),
        sa.Column("email", sa.String(length=250), nullable=False),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    
    # Create the "post" table
    op.create_table(
        "post",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), server_default="", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_post_user_id_users"),
        ),
    )
    
    # Create the "post_tag_association" table (association between posts and tags)
    op.create_table(
        "post_tag_association",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("tag_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["post.id"],
            name=op.f("fk_post_tag_association_post_id_post"),
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tag.id"],
            name=op.f("fk_post_tag_association_tag_id_tag"),
        ),
        sa.UniqueConstraint(
            "post_id", "tag_id", name=op.f("uq_post_tag_association_post_id_tag_id")
        ),
    )

def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_table("post_tag_association")
    op.drop_table("post")
    op.drop_table("users")
    op.drop_table("tag")