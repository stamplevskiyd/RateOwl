"""Added author for tag and title

Revision ID: 35800cec5194
Revises: f59d8f00f516
Create Date: 2025-06-25 12:33:15.847775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35800cec5194'
down_revision: Union[str, Sequence[str], None] = 'f59d8f00f516'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop old useless model (still has no production)
    op.execute("DELETE FROM reviews CASCADE")
    op.execute("DELETE FROM titles CASCADE")
    op.execute("DELETE FROM tags CASCADE")
    op.execute("DELETE FROM tags_to_titles CASCADE")
    op.drop_constraint(op.f('reviews_author_id_fkey'), 'reviews', type_='foreignkey')
    op.drop_constraint(op.f('reviews_title_id_fkey'), 'reviews', type_='foreignkey')
    op.create_foreign_key(None, 'reviews', 'titles', ['title_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'reviews', 'users', ['author_id'], ['id'], ondelete='SET NULL')
    op.add_column('tags', sa.Column('author_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tags', 'users', ['author_id'], ['id'], ondelete='SET NULL')
    op.alter_column('tags_to_titles', 'tag_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('tags_to_titles', 'title_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint(op.f('tags_to_titles_tag_id_fkey'), 'tags_to_titles', type_='foreignkey')
    op.drop_constraint(op.f('tags_to_titles_title_id_fkey'), 'tags_to_titles', type_='foreignkey')
    op.create_foreign_key(None, 'tags_to_titles', 'tags', ['tag_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'tags_to_titles', 'titles', ['title_id'], ['id'], ondelete='cascade')
    op.add_column('titles', sa.Column('author_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'titles', 'users', ['author_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'titles', type_='foreignkey')
    op.drop_column('titles', 'author_id')
    op.drop_constraint(None, 'tags_to_titles', type_='foreignkey')
    op.drop_constraint(None, 'tags_to_titles', type_='foreignkey')
    op.create_foreign_key(op.f('tags_to_titles_title_id_fkey'), 'tags_to_titles', 'titles', ['title_id'], ['id'])
    op.create_foreign_key(op.f('tags_to_titles_tag_id_fkey'), 'tags_to_titles', 'tags', ['tag_id'], ['id'])
    op.alter_column('tags_to_titles', 'title_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('tags_to_titles', 'tag_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'tags', type_='foreignkey')
    op.drop_column('tags', 'author_id')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.create_foreign_key(op.f('reviews_title_id_fkey'), 'reviews', 'titles', ['title_id'], ['id'])
    op.create_foreign_key(op.f('reviews_author_id_fkey'), 'reviews', 'users', ['author_id'], ['id'])
