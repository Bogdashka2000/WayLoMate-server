from sqlalchemy import Text, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk
from datetime import datetime, timezone


class Hotel(Base):
    __tablename__ = 'hotels'

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(300), nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )

    user = relationship("User", back_populates="hotels")