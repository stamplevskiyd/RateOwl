from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b5708d2b55bc"
down_revision: Union[str, Sequence[str], None] = "027b2833eaac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Helpful constants ---------------------------------------------------------
NOW_SQL = sa.text("now()")


def upgrade() -> None:
    # --- REVIEWS -----------------------------------------------------------
    # 1. Add new FK columns as NULLABLE first
    op.add_column("reviews", sa.Column("created_by_fk", sa.Integer(), nullable=True))
    op.add_column("reviews", sa.Column("changed_by_fk", sa.Integer(), nullable=True))

    # 2. Copy data
    op.execute("UPDATE reviews SET created_by_fk = author_id")
    op.execute("UPDATE reviews SET changed_by_fk = author_id")

    # 3. Drop old FK and column
    op.drop_constraint(op.f("reviews_author_id_fkey"), "reviews", type_="foreignkey")
    op.drop_column("reviews", "author_id")

    # 4. Make new FK cols NOT NULL
    op.alter_column("reviews", "created_by_fk", nullable=False)
    op.alter_column("reviews", "changed_by_fk", nullable=False)

    # 5. Add timestamp columns (nullable first -> backfill -> set NOT NULL)
    op.add_column(
        "reviews", sa.Column("created_on", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "reviews", sa.Column("changed_on", sa.DateTime(timezone=True), nullable=True)
    )

    op.execute("UPDATE reviews SET created_on = now(), changed_on = now()")

    op.alter_column("reviews", "created_on", nullable=False)
    op.alter_column("reviews", "changed_on", nullable=False)

    # 6. Drop old timestamp columns
    op.drop_column("reviews", "updated_at")
    op.drop_column("reviews", "created_at")

    # 7. Create new FKs (explicit names to allow clean downgrade)
    op.create_foreign_key(
        "fk_reviews_created_by_users",
        "reviews",
        "users",
        ["created_by_fk"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_reviews_changed_by_users",
        "reviews",
        "users",
        ["changed_by_fk"],
        ["id"],
        ondelete="CASCADE",
    )

    # --- TAGS --------------------------------------------------------------
    op.add_column("tags", sa.Column("created_by_fk", sa.Integer(), nullable=True))
    op.add_column("tags", sa.Column("changed_by_fk", sa.Integer(), nullable=True))
    op.add_column(
        "tags", sa.Column("created_on", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "tags", sa.Column("changed_on", sa.DateTime(timezone=True), nullable=True)
    )

    # Backfill
    op.execute("UPDATE tags SET created_on = now(), changed_on = now()")
    # If you had an author_id-like column, copy it here; otherwise set to system user or 0
    # For now we set both to 1; adjust to your needs
    op.execute(
        "UPDATE tags SET created_by_fk = 1, changed_by_fk = 1 WHERE created_by_fk IS NULL"
    )

    # NOT NULL
    op.alter_column("tags", "created_by_fk", nullable=False)
    op.alter_column("tags", "changed_by_fk", nullable=False)
    op.alter_column("tags", "created_on", nullable=False)
    op.alter_column("tags", "changed_on", nullable=False)

    # FKs
    op.create_foreign_key(
        "fk_tags_created_by_users",
        "tags",
        "users",
        ["created_by_fk"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_tags_changed_by_users",
        "tags",
        "users",
        ["changed_by_fk"],
        ["id"],
        ondelete="CASCADE",
    )

    # Old columns
    op.drop_column("tags", "updated_at")
    op.drop_column("tags", "created_at")

    # --- TITLES ------------------------------------------------------------
    op.add_column("titles", sa.Column("created_by_fk", sa.Integer(), nullable=True))
    op.add_column("titles", sa.Column("changed_by_fk", sa.Integer(), nullable=True))
    op.add_column(
        "titles", sa.Column("created_on", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "titles", sa.Column("changed_on", sa.DateTime(timezone=True), nullable=True)
    )

    op.execute("UPDATE titles SET created_on = now(), changed_on = now()")
    op.execute(
        "UPDATE titles SET created_by_fk = 1, changed_by_fk = 1 WHERE created_by_fk IS NULL"
    )

    op.alter_column("titles", "created_by_fk", nullable=False)
    op.alter_column("titles", "changed_by_fk", nullable=False)
    op.alter_column("titles", "created_on", nullable=False)
    op.alter_column("titles", "changed_on", nullable=False)

    op.create_foreign_key(
        "fk_titles_created_by_users",
        "titles",
        "users",
        ["created_by_fk"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_titles_changed_by_users",
        "titles",
        "users",
        ["changed_by_fk"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_column("titles", "updated_at")
    op.drop_column("titles", "created_at")

    # --- USERS -------------------------------------------------------------
    op.add_column(
        "users", sa.Column("created_on", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "users", sa.Column("changed_on", sa.DateTime(timezone=True), nullable=True)
    )

    op.execute("UPDATE users SET created_on = now(), changed_on = now()")

    op.alter_column("users", "created_on", nullable=False)
    op.alter_column("users", "changed_on", nullable=False)

    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema in the reverse order of upgrade."""
    # --- USERS (reverse of last block) ------------------------------------
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.drop_column("users", "changed_on")
    op.drop_column("users", "created_on")

    # --- TITLES ------------------------------------------------------------
    op.add_column(
        "titles",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "titles",
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.drop_constraint("fk_titles_changed_by_users", "titles", type_="foreignkey")
    op.drop_constraint("fk_titles_created_by_users", "titles", type_="foreignkey")

    op.drop_column("titles", "changed_on")
    op.drop_column("titles", "created_on")
    op.drop_column("titles", "changed_by_fk")
    op.drop_column("titles", "created_by_fk")

    # --- TAGS --------------------------------------------------------------
    op.add_column(
        "tags",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "tags",
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.drop_constraint("fk_tags_changed_by_users", "tags", type_="foreignkey")
    op.drop_constraint("fk_tags_created_by_users", "tags", type_="foreignkey")

    op.drop_column("tags", "changed_on")
    op.drop_column("tags", "created_on")
    op.drop_column("tags", "changed_by_fk")
    op.drop_column("tags", "created_by_fk")

    # --- REVIEWS -----------------------------------------------------------
    op.add_column(
        "reviews",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "reviews",
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column("reviews", sa.Column("author_id", sa.Integer(), nullable=True))

    # Drop new FKs first
    op.drop_constraint("fk_reviews_changed_by_users", "reviews", type_="foreignkey")
    op.drop_constraint("fk_reviews_created_by_users", "reviews", type_="foreignkey")

    # Copy data back (pick created_by_fk as source for author_id)
    op.execute("UPDATE reviews SET author_id = created_by_fk")

    # Recreate old FK
    op.create_foreign_key(
        op.f("reviews_author_id_fkey"),
        "reviews",
        "users",
        ["author_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.drop_column("reviews", "changed_on")
    op.drop_column("reviews", "created_on")
    op.drop_column("reviews", "changed_by_fk")
    op.drop_column("reviews", "created_by_fk")

    # Make author_id NOT NULL if needed (based on your previous schema). If it was NOT NULL:
    op.alter_column("reviews", "author_id", nullable=False)
    # ### end Alembic commands ###
