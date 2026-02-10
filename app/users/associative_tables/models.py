from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk

class UserHobby(Base):

    __tablename__ = 'user_hobby'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    hobby_id = Column(Integer, ForeignKey('hobby.id'), primary_key=True)

    user = relationship("User", back_populates="user_hobbies")
    hobby = relationship("Hobby", back_populates="user_hobbies")

class UserTravelGoal(Base):

    __tablename__ = 'user_travel_goal'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_goal_id = Column(Integer, ForeignKey('travel_goal.id'), primary_key=True)

    user = relationship("User", back_populates="user_travel_goal")
    travel_goal = relationship("", back_populates="user_travel_goal")

class UserLanguage(Base):

    __tablename__ = 'user_language'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    language_id = Column(Integer, ForeignKey('language.id'), primary_key=True)

    user = relationship("User", back_populates="user_language")
    language = relationship("Language", back_populates="user_language")