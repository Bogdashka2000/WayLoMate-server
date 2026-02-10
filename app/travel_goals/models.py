from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk

class TravelGoal(Base):

    __tablename__ = 'travel_goal'

    id: Mapped[int_pk]
    travel_goal_name: Mapped[str]

    user_travel_goals = relationship("UserTravelGoal", back_populates="travel_goal")