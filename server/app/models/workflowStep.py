from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

class WorkflowStep(Base):

    __tablename__ = "workflow_steps"

    id: Mapped[int] = mapped_column(primary_key = True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"))
    name: Mapped[str] = mapped_column(String)
    step_type: Mapped[str] = mapped_column(String, nullable = False)
    config: Mapped[dict] = mapped_column(JSON, nullable = False) 
    order: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    workflow = relationship("Workflow", back_populates = "steps")
