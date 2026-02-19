from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
#from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.schemas import UserRegistrationScheme, UserSearch, UserLoginScheme, UserAvaibleInfo
from typing import List
from app.users.rb import RBUserFilter
from app.users.service import UserService
from app.users.auth import get_hash_password, verify_password, create_token, get_user_by_token
from app.users.image_service import UserImageService
router = APIRouter(prefix='/user', tags=['User Preference'])
# UploadFile = File(..., description="Аватарки и шапка профиля")

@router.get("/")
async def all_users() -> UserAvaibleInfo | dict:
    users = await UserService.find_all_validation_users()
    return {"result" : users}

@router.get("/filter")
async def filtered_users(filters: RBUserFilter = Depends()):
    user = await UserService.find_all_validation_users(**filters.model_dump(exclude_none=True))
    return user

@router.get("/im")
async def authorizated_user(user: User = Depends(get_user_by_token)):
    return user

@router.get("/{id}")
async def current_users(id: int) -> UserAvaibleInfo | dict:
    users = await UserService.find_all_validation_users(id=id)
    return {"result" : users}
    
@router.post("/login")
async def login_user(response: Response, user: UserLoginScheme) -> dict:

    user_in_database = await UserService.find_user_one_or_none(email=user.email)

    if not user_in_database or verify_password(user.password,  user_in_database.password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль')
    token = create_token({"sub": str(user_in_database.id)})
    response.set_cookie(key="user_token", value=token, httponly=True)
    return {
        'ok': True, 
        'user_token': token,
        'refresh_token': None,
        "message": "Пользователь авторизован"
    }
     

@router.post("/registration")
async def register_user(user: UserRegistrationScheme) -> dict:
    exist_user = await UserService.find_user_one_or_none(email = user.email)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')
    user.password = get_hash_password(user.password)
    added_user = await UserService.add_new_user(user)
    return {'result': 'Пользователь зарегистрирован'} 

@router.put('/change_profile_avatar')
async def change_avatar(user: User = Depends(get_user_by_token), 
                        file: UploadFile = File(..., description="Иземенение аватара пользователя")) -> dict: 
    image_link = await UserImageService.save_image(file, 'static_dir_avatar')
    
    
    return {'result': 'ok'}
    

@router.put('/change_profile_header')
async def change_header(file: UploadFile = File(..., description="Иземенение шапки пользователя")) -> dict:
    return await {'result': 'ok'} 

@router.patch('/change_profile')
async def change_profile(user: UserRegistrationScheme) -> dict:
    return await {'result': 'ok'} 

@router.delete('/remove_profile')
async def remove_profile(user: UserSearch) -> dict:
    return await {'result': 'ok'} 
