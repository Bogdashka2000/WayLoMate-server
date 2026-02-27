from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 

class PostInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int = Field(..., description="ID автора")
    text: str = Field(..., description="Текст поста")
    image_url: str = Field(..., description="Ссылка на изображение")
    created_at: datetime = Field(..., description="Время создания поста")
    like_count: int = Field(..., description="Количество лайков")
    comment_count: int = Field(..., description="Количество комментариев")


class AddPost(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    text: str = Field(..., description="Хобби")