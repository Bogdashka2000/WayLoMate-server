from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class HotelInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(..., description="Название отеля")
    description: str = Field(..., description="Описание отеля")
    image_url: str = Field(..., description="URL изображения")
    location: Optional[str] = Field(None, description="Расположение")
    rating: Optional[float] = Field(None, description="Рейтинг")
    created_at: datetime
    user_id: int = Field(..., description="ID пользователя, добавившего отель")


class AddHotel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., description="Название отеля", max_length=200)
    description: str = Field(..., description="Описание отеля")
    image_url: str = Field(..., description="URL изображения")
    location: Optional[str] = Field(None, description="Расположение", max_length=300)
    rating: Optional[float] = Field(None, description="Рейтинг", ge=0, le=5)