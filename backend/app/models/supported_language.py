"""
SupportedLanguage model mapping to the `supported_languages` table.
"""

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin


class SupportedLanguage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "supported_languages"

    language_code: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)
    language_name: Mapped[str] = mapped_column(String(100), nullable=False)
    native_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
