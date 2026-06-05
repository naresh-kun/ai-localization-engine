"""
Translation model mapping to the `translations` table.
"""

import uuid
from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin


class Translation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "translations"

    content_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contents.id", ondelete="CASCADE"), index=True, nullable=False)
    source_language: Mapped[str] = mapped_column(String(10), nullable=False)
    target_language: Mapped[str] = mapped_column(String(10), nullable=False)
    raw_translation: Mapped[str | None] = mapped_column(Text, nullable=True)
    adapted_translation: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True, nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    content = relationship("Content", back_populates="translations")
