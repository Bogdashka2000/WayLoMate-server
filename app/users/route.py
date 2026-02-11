from fastapi import APIRouter, Response, Depends, UploadFile, File
#from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.schemas import UserRegistrationScheme, UserSearch, UserLoginScheme
from typing import List
from app.users.rb import RBUser

router = APIRouter(prefix='/user', tags=['User Preference'])
# UploadFile = File(..., description="Аватарки и шапка профиля")

@router.get("/")
async def all_users():
    return {'result': 'ok'} 

@router.get("/filter")
async def filtered_users(request_body: RBUser = Depends()) -> dict:
    return {'result': 'ok'} 

@router.post("/login")
async def login_user(user: UserLoginScheme) -> dict:
    return {'result': 'ok'} 

@router.post("/registration")
async def register_user(user: UserRegistrationScheme) -> dict:
    return {'result': 'ok'} 

@router.put('/change_profile_avatar')
async def change_avatar(file: UploadFile = File(...)) -> dict:
    return {'result': 'ok'} 

@router.put('/change_profile_header')
async def change_header(file: UploadFile = File(...)) -> dict:
    return {'result': 'ok'} 

@router.patch('/change_profile')
async def change_profile(user: UserRegistrationScheme) -> dict:
    return {'result': 'ok'} 
# @router.put('/cha')

@router.delete('/remove_profile')
async def remove_profile(user: UserSearch) -> dict:
    return {'result': 'ok'} 