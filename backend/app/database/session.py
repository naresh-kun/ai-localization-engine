"""
Database session management.

Creates the SQLAlchemy engine and session factory. Configures connection
pooling parameters from application settings. Provides the `get_db()`
dependency generator for FastAPI route injection.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings


# ── Engine ───────────────────────────────────────────────────────────────────
# The engine manages the connection pool to PostgreSQL.

engine = create_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,
    echo=settings.debug,
)


# ── Session Factory ──────────────────────────────────────────────────────────
# SessionLocal creates new database sessions bound to the engine.

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# ── Dependency ───────────────────────────────────────────────────────────────
# Yields a session per request and ensures cleanup after the request completes.

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Yields a SQLAlchemy session and ensures it is closed after the
    request is complete, returning the connection to the pool.

    Usage:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
