from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
#from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.schemas import UserRegistrationScheme, UserSearch, UserLoginScheme, UserAvaibleInfo, HobbyInfo, GoalInfo, LanguageInfo
from typing import List
from app.users.rb import RBUserFilter
from app.users.service import UserService
from app.users.auth import get_hash_password, verify_password, create_token, get_user_by_token
from app.users.image_service import UserImageService

router = APIRouter(prefix='/user', tags=['User Preference'])
# UploadFile = File(..., description="Аватарки и шапка профиля")

@router.get("/", response_model=List[UserAvaibleInfo])
async def all_users() -> UserAvaibleInfo | dict:
    users = await UserService.find_all_validation_users()
    return users

@router.get("/filter", response_model=List[UserAvaibleInfo])
async def filtered_users(filters: RBUserFilter = Depends()):
    user = await UserService.find_all_validation_users(**filters.model_dump(exclude_none=True))
    return user

@router.get("/im", response_model=UserAvaibleInfo)
async def authorizated_user(user: User = Depends(get_user_by_token)):
    return user[0]

@router.get("/{id}", response_model=UserAvaibleInfo)
async def current_users(id: int) -> UserAvaibleInfo | dict:
    user = await UserService.find_all_validation_users(id=id)
    return user[0]

@router.get("/{id}/hobbies", response_model=List[HobbyInfo])
async def users_hobbies(id: int) -> List[HobbyInfo]:
    hobby = await UserService.find_hobbies_by_user_id(id)
    return hobby

@router.get("/{id}/goals", response_model=List[GoalInfo])
async def user_goals(id: int) -> List[GoalInfo]:
    goals = await UserService.find_goals_by_user_id(id)
    return goals

@router.get("/{id}/languages", response_model=List[LanguageInfo])
async def user_languages(id: int) -> List[LanguageInfo]:
    languages = await UserService.find_languages_by_user_id(id)
    return languages
    
@router.post("/login")
async def login_user(response: Response, user: UserLoginScheme) -> dict:
    user_in_database = await UserService.find_user_one_or_none(email=user.email)
    if not user_in_database or verify_password(user.password,  user_in_database.password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль')
    token = create_token({"sub": str(user_in_database.id)})
    response.set_cookie(key="user_token", value=token, httponly=True)
    return { 'ok': True, 'user_token': token, 'refresh_token': None, "message": "Пользователь авторизован" }
     
@router.post("/registration")
async def register_user(user: UserRegistrationScheme) -> dict:
    exist_user = await UserService.find_user_one_or_none(email = user.email)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')
    user.password = get_hash_password(user.password)
    added_user = await UserService.add_new_user(user)
    return {'result': 'Пользователь зарегистрирован'} 

@router.patch('/change_profile_avatar')
async def change_avatar(user: User = Depends(get_user_by_token), 
                        file: UploadFile = File(..., description="Иземенение аватара пользователя")) -> UserAvaibleInfo | dict: 
    image_name = await UserImageService.save_image(file, 'static_dir_avatar')
    new_user = await UserService.change_user_avatar(user[0], image_name)
    return new_user
    
@router.patch('/change_profile_header')
async def change_header(user: User = Depends(get_user_by_token), 
                        file: UploadFile = File(..., description="Иземенение шапки пользователя")) -> UserAvaibleInfo | dict: 
    image_name = await UserImageService.save_image(file, 'static_dir_header')
    new_user = await UserService.change_user_header(user[0], image_name)
    return new_user 

@router.patch('/change_profile')
async def change_profile(user: User = Depends(get_user_by_token), filters: RBUserFilter = Depends()) -> dict:
    changed_user = await UserService.change_user_info(user[0], **filters.model_dump(exclude_none=True))
    return {'result': 'Данные изменены'} 

@router.delete('/logout')
async def logout_user(response: Response) -> dict:
    response.delete_cookie(key="user_token")
    return { 'ok': True, "message": "Пользователь вышел" }

@router.delete('/remove_profile')
async def remove_profile(user: User = Depends(get_user_by_token)) -> dict:
    removed_user = await UserService.remove_user(user[0])
    return {'result': 'Пользователь удалён'} 
