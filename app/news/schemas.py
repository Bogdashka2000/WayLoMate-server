from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 

class NewsInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int = Field(..., description="ID автора")
    title: str = Field(..., description="Заголовок новости")
    text: str = Field(..., description="Текст новости")



class AddNews(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str = Field(..., description="Заголовок новости")
    text: str = Field(..., description="Текст новости")