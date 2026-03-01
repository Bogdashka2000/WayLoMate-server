from sqlalchemy import Text, String, Boolean, Integer, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from app.database import Base, int_pk
from datetime import datetime
import enum

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int_pk]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    subscriber_to_id: Mapped[int] = mapped_column( ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="subscriptions_made")
    subscribed_to: Mapped["User"] = relationship("User", foreign_keys=[subscriber_to_id], back_populates="subscriptions_received")

    __table_args__ = (
        UniqueConstraint('user_id', 'subscriber_to_id', name='uq_subscription_pair'),
        Index('idx_subscriptions_user_id', 'user_id'),
        Index('idx_subscriptions_subscriber_to_id', 'subscriber_to_id'),
    )