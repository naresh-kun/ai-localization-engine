"""
SQLAlchemy model base and common mixins.

Provides the declarative base class and reusable mixins for timestamps
and soft-delete functionality. All ORM models inherit from Base and
compose the mixins they need.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Boolean, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Declarative base for all SQLAlchemy models.

    All models inherit from this class. Alembic uses it to discover
    models for auto-generated migrations.
    """
    pass


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at timestamp columns.

    Both columns use timezone-aware UTC timestamps. updated_at is
    automatically refreshed on every UPDATE.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Mixin that adds soft-delete support via a deleted_at column.

    When a record is "deleted", the deleted_at column is set to the
    current UTC timestamp instead of removing the row. Queries should
    filter on `deleted_at IS NULL` to exclude soft-deleted records.
    """

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )


class UUIDPrimaryKeyMixin:
    """
    Mixin that adds a UUID primary key column.

    Generates a UUID v4 as the default value. Uses SQLAlchemy's cross-database
    Uuid type, stored natively where supported, or as a string/binary otherwise.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
