from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    github_url: Mapped[str] = mapped_column(String)

    description : Mapped[str | None] = mapped_column(String, nullable = True)