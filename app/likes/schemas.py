from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 

class LikeInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    action: str = Field(..., description="Событие")
    is_liked: bool = Field(..., description="Проверка на лайк")
    total_likes: int = Field(..., description="Общее количество лайков")


class AddLike(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    post_id: int = Field(..., description="ID поста")