from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    github_repo_id: Mapped[int] = mapped_column(
        Integer,
    )

    name: Mapped[str] = mapped_column(String)

    github_url: Mapped[str] = mapped_column(String)

    clone_url: Mapped[str] = mapped_column(String)

    default_branch: Mapped[str] = mapped_column(String)

    private: Mapped[bool] = mapped_column(Boolean)

    description : Mapped[str | None] = mapped_column(String, nullable = True)

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates = "repositories")

    workflows = relationship(
        "Workflow",
        back_populates = "repository",
        cascade = "all, delete-orphan"
    )