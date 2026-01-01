"""
SQLAlchemy declarative base for database models.

All database models should inherit from this Base class
to ensure they are properly registered with SQLAlchemy.

IMPORTANT: This file also imports all models to ensure they are registered
with SQLAlchemy's metadata before Alembic runs auto-migrations.
When adding a new model, import it here!
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    All model classes should inherit from this Base to ensure
    they are properly integrated with SQLAlchemy's ORM system.

    Example:
        from app.db.base import Base

        class User(Base):
            __tablename__ = "users"
            # ... model definition
    """

    pass


# =============================================================================
# IMPORTANT: Import all models here for Alembic auto-migrations
# =============================================================================
# Alembic uses Base.metadata to detect models. Models must be imported
# AFTER Base is defined so they can inherit from it. Add new models below.
#
# This ensures that when Alembic does:
#   from app.db.base import Base
# All models are already registered in Base.metadata

from app.models.job import Job  # noqa: E402, F401
from app.models.application import Application  # noqa: E402, F401
