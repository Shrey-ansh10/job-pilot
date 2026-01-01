"""
Job Model - Stores scraped job listings with AI embeddings for matching.

This model represents jobs scraped from various job boards (Indeed, Greenhouse, etc.).
Each job has an embedding vector (1536 dimensions) for semantic similarity matching
with the user's resume using pgvector.

Workflow:
1. Scraper creates job with status='new'
2. Matching service calculates embedding + match_score, sets status='processed'
3. User applies, status='applied' or 'rejected'
"""

import uuid
from datetime import date, datetime
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Date, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Job(Base):
    """
    Represents a scraped job listing.

    Key fields:
    - embedding: 1536-dim vector for semantic search (OpenAI ada-002 compatible)
    - match_score: 0-100 indicating how well user's resume matches this job
    - status: tracks job through the pipeline (new -> processed -> applied/rejected)
    """

    __tablename__ = "jobs"

    # Primary key - UUID for distributed-friendly IDs
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the job"
    )

    # Source tracking - where did this job come from?
    external_job_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Job ID from the source website (for deduplication)"
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Source job board: 'indeed', 'greenhouse', 'linkedin', etc."
    )

    # Core job information
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Company name"
    )
    job_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Job title/position"
    )
    job_url: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
        comment="URL to apply (unique to prevent duplicate applications)"
    )
    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Job location (city, remote, hybrid, etc.)"
    )

    # Salary information (optional - not all jobs list salary)
    salary_min: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        comment="Minimum salary (if listed)"
    )
    salary_max: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        comment="Maximum salary (if listed)"
    )

    # Job content - the meat of the listing
    job_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Full job description text"
    )
    requirements: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Job requirements/qualifications (if separately listed)"
    )

    # Dates
    posted_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="When the job was posted (if available)"
    )
    scraped_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        comment="When we scraped this job"
    )

    # AI matching fields - populated by matching_service
    embedding: Mapped[Optional[list]] = mapped_column(
        Vector(1536),  # OpenAI ada-002 embedding dimension
        nullable=True,
        comment="Job description embedding for semantic similarity search"
    )
    match_score: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2),  # 0.00 to 100.00
        nullable=True,
        comment="Match score 0-100 (how well resume matches this job)"
    )

    # Status tracking - where is this job in our pipeline?
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="new",
        comment="Pipeline status: 'new', 'processed', 'applied', 'rejected'"
    )

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        comment="Record creation timestamp"
    )

    def __repr__(self) -> str:
        return f"<Job {self.job_title} at {self.company_name} (status={self.status})>"


# Indexes for common query patterns
# These are created separately to keep the model class clean

# Fast filtering by status (most common query)
Index("idx_jobs_status", Job.status)

# Sort by match score to show best matches first
Index("idx_jobs_match_score", Job.match_score.desc())

# Vector similarity search using IVFFlat (approximate nearest neighbor)
# lists=100 is good for up to ~1M rows, adjust if dataset grows
Index(
    "idx_jobs_embedding",
    Job.embedding,
    postgresql_using="ivfflat",
    postgresql_with={"lists": 100},
    postgresql_ops={"embedding": "vector_cosine_ops"}
)
