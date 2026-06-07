from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    github_id: Mapped[int |  None] = mapped_column(Integer, unique= True, nullable=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique= True)
    created_at: Mapped[datetime] = mapped_column(datetime, default=datetime.now)
    hashed_password: Mapped[str] = mapped_column(String)
