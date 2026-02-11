from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk
from datetime import date
import enum

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'

class User(Base):

    __tablename__ = 'users'

    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    birthday: Mapped[date]
    gender: Column(Enum(Gender))
    about: Mapped[str] = mapped_column(Text)
    header_image_url: Mapped[str]
    avatar_image_url: Mapped[str]

    user_hobbies = relationship("UserHobby", back_populates="user", cascade="all, delete-orphan")
    user_travel_goals = relationship("UserTravelGoal", back_populates="user", cascade="all, delete-orphan")
    user_languages = relationship("UserLanguage", back_populates="user", cascade="all, delete-orphan")