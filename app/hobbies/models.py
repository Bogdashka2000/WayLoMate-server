from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk

class Hobby(Base):

    __tablename__ = 'hobby'

    id: Mapped[int_pk]
    hobby_name: Mapped[str]

    user_hobbies = relationship("UserHobby", back_populates="hobby")