from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class OAuthState(Base):
    __tablename__ = "oauth_states"

    state: Mapped[str] = mapped_column(
        String,
        primary_key = True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    created_at: Mapped[datetime]