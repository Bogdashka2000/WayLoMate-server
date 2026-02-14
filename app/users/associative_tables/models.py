from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.users.models import User
from app.hobbies.models import Hobby
from app.languages.models import Language
from app.travel_goals.models import TravelGoal

class UserHobby(Base):
    __tablename__ = 'user_hobby'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    hobby_id: Mapped[int] = mapped_column(ForeignKey('hobbies.id'), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="user_hobbies")
    hobby: Mapped["Hobby"] = relationship(back_populates="user_hobbies")


class UserTravelGoal(Base):
    __tablename__ = 'user_travel_goal'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    travel_goal_id: Mapped[int] = mapped_column(ForeignKey('travel_goals.id'), primary_key=True) 

    user: Mapped["User"] = relationship(back_populates="user_travel_goals")
    travel_goal: Mapped["TravelGoal"] = relationship(back_populates="user_travel_goals")


class UserLanguage(Base):
    __tablename__ = 'user_language'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey('languages.id'), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="user_languages")
    language: Mapped["Language"] = relationship(back_populates="user_languages")