from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 

class CommentInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int = Field(..., description="ID автора")
    post_id: int = Field(..., description="ID поста")
    text: str = Field(..., description="Текст комментария")
    created_at: datetime = Field(..., description="Время создания комментария")


class AddComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    post_id: int = Field(..., description="ID поста")
    text: str = Field(..., description="Текст комментария")