from sqlalchemy import Text, String, Boolean, Integer, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from app.database import Base, int_pk
import datetime
from pydantic import EmailStr
import enum

class Like(Base):

    __tablename__ = 'likes'

    id: Mapped[int_pk]
    
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow())
    
    user: Mapped["User"] = relationship("User", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='uq_user_post_like'),
        Index('idx_likes_post_id', 'post_id'),
        Index('idx_likes_user_id', 'user_id'),
    )
