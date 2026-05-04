"""Initial revision

Revision ID: a2fa5795f444
Revises: 
Create Date: 2026-02-14 21:01:08.589385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a2fa5795f444'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # ========================================================================
    # 1. БАЗОВЫЕ ТАБЛИЦЫ (создаём ПЕРВЫМИ — на них ссылаются внешние ключи)
    # ========================================================================
    
    # ── hobbies ──────────────────────────────────────────────────────────
    op.create_table('hobbies',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('hobby_name', sa.String(length=40), nullable=False),
        sa.UniqueConstraint('hobby_name', name='uq_hobbies_name')
    )
    
    # ── languages ────────────────────────────────────────────────────────
    op.create_table('languages',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('language_name', sa.String(length=40), nullable=False),
        sa.UniqueConstraint('language_name', name='uq_languages_name')
    )
    
    # ── travel_goals ─────────────────────────────────────────────────────
    op.create_table('travel_goals',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('travel_goal_name', sa.String(length=40), nullable=False),
        sa.UniqueConstraint('travel_goal_name', name='uq_travel_goals_name')
    )
    
    # ── users ────────────────────────────────────────────────────────────
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('first_name', sa.String(length=20), nullable=False),
        sa.Column('last_name', sa.String(length=20), nullable=False),
        sa.Column('birthday', sa.Date(), nullable=False),
        sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
        sa.Column('about', sa.Text(), nullable=False),
        sa.Column('header_image_url', sa.String(length=255), nullable=False),
        sa.Column('avatar_image_url', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=48), nullable=False),
        sa.Column('email', sa.String(length=20), nullable=False),
        # created_at / updated_at намеренно опущены (см. ваш downgrade)
    )
    
    # ========================================================================
    # 2. СВЯЗУЮЩИЕ ТАБЛИЦЫ (создаём ПОСЛЕ базовых — когда есть на что ссылаться)
    # ========================================================================
    
    # ── user_hobby ───────────────────────────────────────────────────────
    op.create_table('user_hobby',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('hobby_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['hobby_id'], ['hobbies.id'], name='fk_user_hobby_hobby'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_hobby_user'),
        sa.PrimaryKeyConstraint('user_id', 'hobby_id', name='pk_user_hobby')
    )
    
    # ── user_language ────────────────────────────────────────────────────
    op.create_table('user_language',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('language_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['language_id'], ['languages.id'], name='fk_user_language_lang'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_language_user'),
        sa.PrimaryKeyConstraint('user_id', 'language_id', name='pk_user_language')
    )
    
    # ── user_travel_goal ─────────────────────────────────────────────────
    op.create_table('user_travel_goal',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('travel_goal_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['travel_goal_id'], ['travel_goals.id'], name='fk_user_travel_goal_goal'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_travel_goal_user'),
        sa.PrimaryKeyConstraint('user_id', 'travel_goal_id', name='pk_user_travel_goal')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем в ОБРАТНОМ порядке: сначала связующие, потом базовые таблицы
    
    op.drop_table('user_travel_goal')
    op.drop_table('user_language')
    op.drop_table('user_hobby')
    op.drop_table('users')
    op.drop_table('travel_goals')
    op.drop_table('languages')
    op.drop_table('hobbies')