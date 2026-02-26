from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 


class LanguageInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    language_name: str = Field(..., description="Язык")

class AddLanguage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    language_name: str = Field(..., description="Язык")