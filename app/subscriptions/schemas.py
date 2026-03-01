from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 

class ToggleResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    action: str = Field(..., description="Событие")
    is_subscribed: bool = Field(..., description="Проверка на подписку")


class AddSub(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    user_id: int = Field(..., description="ID пользователя, на которого будет оформлена подписка")