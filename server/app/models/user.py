from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    github_id: Mapped[int] = mapped_column(Integer, unique= True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique= True)
    created_at: Mapped[str] = mapped_column(String)
