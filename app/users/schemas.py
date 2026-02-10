from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date

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


class UserConfirmEmailScheme(BaseModel):
    confirm_code: int = Field(..., min_length=6, max_length=6, description="Введите код для подтверждения")

class UserLoginScheme(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=48, description="Введите пароль")

