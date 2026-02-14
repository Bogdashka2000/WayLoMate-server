from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk
from sqlalchemy import String

class TravelGoal(Base):

    __tablename__ = 'travel_goals'

    id: Mapped[int_pk]
    travel_goal_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)

    user_travel_goals = relationship("UserTravelGoal", back_populates="travel_goal")