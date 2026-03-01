from sqlalchemy import Text, String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from app.database import Base, int_pk
from datetime import date
from pydantic import EmailStr
import enum

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'

class User(Base):

    __tablename__ = 'users'

    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=True) 
    gender: Mapped[Gender] = mapped_column(SQLEnum(Gender)) 
    about: Mapped[str] = mapped_column(Text)
    header_image_url: Mapped[str] = mapped_column(String(255), default="none")
    avatar_image_url: Mapped[str] = mapped_column(String(255),default="none")
    password: Mapped[str] = mapped_column(String(1024), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    user_hobbies = relationship("UserHobby", back_populates="user", cascade="all, delete-orphan")
    user_travel_goals = relationship("UserTravelGoal", back_populates="user", cascade="all, delete-orphan")
    user_languages = relationship("UserLanguage", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

    subscriptions_made: Mapped[list["Subscription"]] = relationship(
        "Subscription", 
        foreign_keys="Subscription.user_id", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    subscriptions_received: Mapped[list["Subscription"]] = relationship(
        "Subscription", 
        foreign_keys="Subscription.subscriber_to_id", 
        back_populates="subscribed_to", 
        cascade="all, delete-orphan"
    )