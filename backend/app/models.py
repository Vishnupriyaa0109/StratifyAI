from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(80), default="In-app")
    segment: Mapped[str] = mapped_column(String(100), default="Unknown")
    text: Mapped[str] = mapped_column(Text)
    theme: Mapped[str] = mapped_column(String(100), default="Other", index=True)
    sentiment: Mapped[str] = mapped_column(String(20), default="neutral", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Opportunity(Base):
    __tablename__ = "opportunities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(180))
    problem_statement: Mapped[str] = mapped_column(Text)
    theme: Mapped[str] = mapped_column(String(100), default="Other")
    reach: Mapped[float] = mapped_column(Float, default=1)
    impact: Mapped[float] = mapped_column(Float, default=1)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    effort: Mapped[float] = mapped_column(Float, default=1)
    status: Mapped[str] = mapped_column(String(30), default="Candidate")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Experiment(Base):
    __tablename__ = "experiments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(180))
    hypothesis: Mapped[str] = mapped_column(Text)
    success_metric: Mapped[str] = mapped_column(String(180))
    baseline_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Planned")
    owner: Mapped[str] = mapped_column(String(100), default="Product")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
