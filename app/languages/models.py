from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk
from sqlalchemy import String

class Language(Base):

    __tablename__ = 'languages'

    id: Mapped[int_pk]
    language_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)

    user_languages = relationship("UserLanguage", back_populates="language")