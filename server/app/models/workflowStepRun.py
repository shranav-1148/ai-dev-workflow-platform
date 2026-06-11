from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class WorkflowStepRun(Base):
    __tablename__ = "workflow_step_run"

    id: Mapped[int] = mapped_column(primary_key = True)

    workflow_run_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_runs.id"),
        nullable = False
    )

    workflow_step_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_steps.id"),
        nullable =False
    )

    status: Mapped[str] = mapped_column(String)

    output: Mapped[dict | None] = mapped_column(JSON)

    error_message: Mapped[str | None] = mapped_column(String)

    started_at: Mapped[datetime] = mapped_column(
        server_default = func.now()
    )

    completed_at: Mapped[datetime | None]