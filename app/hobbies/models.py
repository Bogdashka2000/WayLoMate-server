from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk
from sqlalchemy import String

class Hobby(Base):

    __tablename__ = 'hobbies'

    id: Mapped[int_pk]
    hobby_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)

    user_hobbies = relationship("UserHobby", back_populates="hobby", cascade="all, delete-orphan")