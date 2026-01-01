"""
Database Models Package

This module exports all SQLAlchemy models for the job application system.
Import models from here for clean imports throughout the application.

Example:
    from app.models import Job, Application

Models:
    - Job: Scraped job listings with embeddings for matching
    - Application: Job applications with generated documents
"""

from app.models.application import Application
from app.models.job import Job

# Export all models - this list is used by Alembic for auto-migrations
__all__ = [
    "Job",
    "Application",
]
