from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class PlaceInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(..., description="Название места")
    description: str = Field(..., description="Описание места")
    image_url: str = Field(..., description="URL изображения")
    location: Optional[str] = Field(None, description="Расположение")
    category: Optional[str] = Field(None, description="Категория")
    created_at: datetime
    user_id: int = Field(..., description="ID пользователя, добавившего место")


class AddPlace(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., description="Название места", max_length=200)
    description: str = Field(..., description="Описание места")
    image_url: str = Field(..., description="URL изображения")
    location: Optional[str] = Field(None, description="Расположение", max_length=300)
    category: Optional[str] = Field(None, description="Категория", max_length=100)