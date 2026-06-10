from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id:Mapped[int]  = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id")
    )

    repository = relationship("Repository", back_populates="workflows")

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default = func.now(),
        onupdate=func.now()
    )

    steps = relationship("WorkflowStep", back_populates = "workflow", cascade="all, delete-orphan")

    runs = relationship("WorkflowRun", back_populates = "workflow", cascade = "all, delete-orphan")
