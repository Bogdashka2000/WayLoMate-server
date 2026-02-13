from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk

class Language(Base):

    __tablename__ = 'language'

    id: Mapped[int_pk]
    language_name: Mapped[str]

    user_languages = relationship("UserLanguage", back_populates="language")