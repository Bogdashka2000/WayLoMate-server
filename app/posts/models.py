from sqlalchemy import Text, String, DateTime, ForeignKey, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from app.database import Base, int_pk
from datetime import datetime
from app.likes.models import Like
from app.comments.models import Comment


class Post(Base):

    __tablename__ = 'posts'

    id: Mapped[int_pk]
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), default="none")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    user = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    