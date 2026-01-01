"""
Application Model - Tracks job applications and their generated documents.

This model represents an application to a specific job. It stores:
- Reference to the job being applied to
- Paths to generated resume and cover letter files
- Text content of generated documents (for display/search)
- Application status and submission tracking
- Screenshot of filled form (for review before submission)

Workflow:
1. User selects a job to apply to
2. System generates customized resume + cover letter -> status='draft'
3. Automation fills form, takes screenshot -> ready for review
4. User approves -> status='submitted'
5. If error occurs -> status='failed' with error_message
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Application(Base):
    """
    Represents a job application with its generated documents.

    Key fields:
    - job_id: Links to the Job being applied to
    - resume_path/cover_letter_path: File paths to generated PDFs
    - resume_text/cover_letter_text: Text content for display/search
    - screenshot_path: Pre-submission screenshot for manual review
    - status: 'draft' -> 'submitted' -> 'failed'
    """

    __tablename__ = "applications"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for the application"
    )

    # Foreign key to jobs table
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        comment="Reference to the job being applied to"
    )

    # Denormalized job info for quick access (avoids joins for common queries)
    # These are copied from Job at application creation time
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Company name (denormalized from Job)"
    )
    job_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Job title (denormalized from Job)"
    )
    job_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Application URL (denormalized from Job)"
    )

    # Generated resume - customized for this specific job
    resume_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Path to customized resume PDF (e.g., 'storage/resumes/{job_id}.pdf')"
    )
    resume_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Generated resume text content (markdown/plain text)"
    )

    # Generated cover letter - tailored for this job
    cover_letter_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Path to cover letter PDF (e.g., 'storage/cover_letters/{job_id}.pdf')"
    )
    cover_letter_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Generated cover letter text content"
    )

    # Screenshot of filled application form (for manual review before submission)
    screenshot_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Path to pre-submission screenshot (e.g., 'storage/screenshots/{job_id}.png')"
    )

    # Application status tracking
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
        comment="Application status: 'draft', 'submitted', 'failed'"
    )

    # Timestamps
    application_date: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        comment="When the application was prepared/created"
    )
    submitted_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
        comment="When the application was actually submitted (null if not yet)"
    )

    # Notes and error tracking
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="User notes about this application"
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Error details if application failed"
    )

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        comment="Record creation timestamp"
    )

    # Relationship to Job model (for easy access via application.job)
    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="applications",
        lazy="selectin"  # Eager load job when loading application
    )

    def __repr__(self) -> str:
        return f"<Application {self.job_title} at {self.company_name} (status={self.status})>"


# Import Job here to avoid circular imports (for type hints in relationship)
from app.models.job import Job  # noqa: E402

# Add reverse relationship to Job model
# This allows: job.applications to get all applications for a job
Job.applications = relationship(
    "Application",
    back_populates="job",
    cascade="all, delete-orphan",
    lazy="selectin"
)
