from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    github_url: Mapped[str] = mapped_column(String)

    description : Mapped[str | None] = mapped_column(String, nullable = True)

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates = "repositories")

    workflows = relationship(
        "Workflow",
        back_populates = "repository",
        cascade = "all, delete-orpahn"
    )