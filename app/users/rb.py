from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


class RBUserFilter(BaseModel):
    id: Optional[int] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    birthday: Optional[date] = Field(default=None)
    gender: Optional[str] = Field(default=None)


    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
