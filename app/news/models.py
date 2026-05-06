from sqlalchemy import Text, String, DateTime, ForeignKey, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from app.database import Base, int_pk
from datetime import datetime, timezone
from app.likes.models import Like
from app.comments.models import Comment


class News(Base):

    __tablename__ = 'news'

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    text: Mapped[str] = mapped_column(String(2000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    user = relationship("User", back_populates="news")
    