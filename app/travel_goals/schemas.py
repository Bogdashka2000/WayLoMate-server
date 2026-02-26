from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 


class GoalInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    travel_goal_name: str = Field(..., description="Цель путешествий")

class AddGoal(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    travel_goal_name: str = Field(..., description="Цель путешествий")