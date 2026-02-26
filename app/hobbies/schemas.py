from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 


class HobbyInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hobby_name: str = Field(..., description="Хобби")

class AddHobby(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    hobby_name: str = Field(..., description="Хобби")