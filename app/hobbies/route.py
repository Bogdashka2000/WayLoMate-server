from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.hobbies.service import HobbyService
from app.hobbies.schemas import HobbyInfo, AddHobby
from app.users.auth import get_admin_by_token
from typing import List

router = APIRouter(prefix='/hobby', tags=['Hobby Preference'])

@router.get("/", response_model=List[HobbyInfo])
async def all_hobbies():
    hobbies = await HobbyService.all_hobbies()
    return hobbies

@router.post("/add", response_model=HobbyInfo)
async def create_new_hobby(hobby: AddHobby, is_admin: bool = Depends(get_admin_by_token)):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У пользователя нет прав администратора')
    hobby = await HobbyService.add_hobby(hobby)
    return hobby

@router.delete("/remove/{id}")
async def remove_hobby(id: int):
    hobby = await HobbyService.remove_hobby(id)
    return hobby