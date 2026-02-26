from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.languages.service import LanguageService
from app.languages.schemas import LanguageInfo, AddLanguage
from app.users.auth import get_admin_by_token
from typing import List

router = APIRouter(prefix='/language', tags=['Language Preference'])

@router.get("/", response_model=List[LanguageInfo])
async def all_languages():
    languages = await LanguageService.all_languages()
    return languages

@router.post("/add", response_model=LanguageInfo)
async def create_new_language(language: AddLanguage, is_admin: bool = Depends(get_admin_by_token)):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У пользователя нет прав администратора')
    language = await LanguageService.add_language(language)
    return language

@router.delete("/remove/{id}")
async def remove_language(id: int):
    language = await LanguageService.remove_language(id)
    return language