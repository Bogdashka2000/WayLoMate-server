from fastapi import APIRouter, Response, Depends, UploadFile, File
#from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.schemas import UserRegistrationScheme, UserSearch, UserLoginScheme
from typing import List
from app.users.rb import RBUserFilter
from app.users.service import UserService

router = APIRouter(prefix='/user', tags=['User Preference'])
# UploadFile = File(..., description="Аватарки и шапка профиля")

@router.get("/")
async def all_users():
    return await {'result': 'ok'} 

@router.get("/{id}")
async def current_users(student_id: int) -> dict:
    return await {'result': 'ok'} 

@router.get("/filter")
async def filtered_users(request_body: RBUserFilter = Depends()) -> dict:
    return await {'result': 'ok'} 

@router.post("/login")
async def login_user(user: UserLoginScheme) -> dict:
    return await {'result': 'ok'} 

@router.post("/registration")
async def register_user(user: UserRegistrationScheme) -> dict:
    await UserService.addNewUser(user)
    return {'result': 'ok'}

@router.put('/change_profile_avatar')
async def change_avatar(file: UploadFile = File(...)) -> dict:
    return await {'result': 'ok'} 

@router.put('/change_profile_header')
async def change_header(file: UploadFile = File(...)) -> dict:
    return await {'result': 'ok'} 

@router.patch('/change_profile')
async def change_profile(user: UserRegistrationScheme) -> dict:
    return await {'result': 'ok'} 
# @router.put('/cha')

@router.delete('/remove_profile')
async def remove_profile(user: UserSearch) -> dict:
    return await {'result': 'ok'} 
