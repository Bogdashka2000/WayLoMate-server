from app.database import async_session_maker
from sqlalchemy import select
from app.languages.models import Language
from sqlalchemy.ext.asyncio import AsyncSession
from app.languages.schemas import AddLanguage
from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException


class LanguageService:
    
    @classmethod
    async def language_by_id(cls, session: AsyncSession, language_id: int):  
        check = await session.execute(select(Language).filter_by(id=language_id))
        language_in_db = check.scalars().one_or_none()
        if not language_in_db:
            raise HTTPException(status_code=404, detail="Язык не найден")
        return language_in_db

    @classmethod
    async def all_languages(cls):
        async with async_session_maker() as session:
            languages_execute = await session.execute(select(Language))
            return languages_execute.scalars().all()

    @classmethod
    async def add_language(cls, language_data: AddLanguage):
        async with async_session_maker() as session:
            
            check = await session.execute(select(Language).filter_by(language_name=language_data.language_name))
            if check.scalars().one_or_none():
                raise HTTPException(status_code=404, detail="Язык уже существует")


            language = Language(**language_data.model_dump())
            session.add(language)
            await session.flush() 
            await session.commit()
            await session.refresh(language)
            return language

    @classmethod
    async def remove_language(cls, id: int):
        async with async_session_maker() as session:
            language = await cls.language_by_id(session, id)
            await session.delete(language)
            await session.commit()
            return {"result": "Язык удалён"}