from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[int] = mapped_column(primary_key = True)

    workflow_id: Mapped[int] = mapped_column(
        ForeignKey("workflows.id"),
        nullable = False
    )

    status: Mapped[str] = mapped_column(String)

    started_at: Mapped[datetime]  = mapped_column(
        server_default=func.now()
    )

    completed_at: Mapped[datetime | None]

    workflow = relationship(
        "Workflow",
        back_populates = "runs"
    )

