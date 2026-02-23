from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import date, datetime 

class UserRegistrationScheme(BaseModel):
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str = Field(..., description="Фамилия пользователя")
    birthday: date = Field(..., description="Дата рождения")
    gender: str = Field(..., description="Введите гендер: 'male' или 'female'")
    hobbies: list[int] = Field(..., description="Введите все id хобби")
    goals: list[int] = Field(..., description="Введите все id целей")
    languages: list[int] = Field(..., description="Введите все id языков")
    about: str = Field(..., max_length=200, description="О себе")
    password: str = Field(..., min_length=8, max_length=48, description="Введите пароль")
    email: EmailStr = Field(..., description="Электронная почта")


    @field_validator("gender")
    @classmethod 
    def validate_gender(cls, value: str) -> str:
        if value not in ["male", "female"]:
            raise ValueError("Гендер должен быть 'male' или 'female'")
        return value

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, value: date) -> date:
        if value and value >= datetime.now().date():
            raise ValueError('Будущее время при рождении ')
        return value
    
    def user_hobbies_model_dump(self):
        return self.hobbies

    def user_goals_model_dump(self):
        return self.goals
    
    def user_languages_model_dump(self):
        return self.languages


class UserConfirmEmailScheme(BaseModel):
    confirm_code: str = Field(..., min_length=6, max_length=6, description="Введите код для подтверждения")

class UserLoginScheme(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=48, description="Введите пароль")

class UserSearch(BaseModel):
    profile_id: str

class UserAvaibleInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str = Field(..., description="Фамилия пользователя")
    birthday: date = Field(..., description="Дата рождения")
    gender: str = Field(..., description="Гендер: 'male' или 'female'")
    avatar_image_url: str = Field(..., description="Аватарка пользователя")
    header_image_url: str = Field(..., description="Шапка пользователя")
    # hobbies: list[str] = Field(..., description="Введите все id хобби")
    # goals: list[str] = Field(..., description="Введите все id целей")
    # languages: list[str] = Field(..., description="Введите все id языков")
    about: str = Field(..., max_length=200, description="О себе")
    # password: str = Field(..., min_length=8, max_length=48, description="Введите пароль")
    # email: EmailStr = Field(..., description="Электронная почта")

class HobbyInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # id: int
    hobby_name: str = Field(..., description="Хобби")

class GoalInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # id: int
    travel_goal_name: str = Field(..., description="Цели")

class LanguageInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # id: int
    language_name: str = Field(..., description="Язык, на котором пользователь говорит")

