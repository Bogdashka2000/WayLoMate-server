from app.database import async_session_maker
from sqlalchemy import select
from app.hobbies.models import Hobby
from sqlalchemy.ext.asyncio import AsyncSession
from app.hobbies.schemas import AddHobby
from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException


class HobbyService:
    
    @classmethod
    async def hobby_by_id(cls, session: AsyncSession, hobby_id: int):  
        check = await session.execute(select(Hobby).filter_by(id=hobby_id))
        hobby_in_db = check.scalars().one_or_none()
        if not hobby_in_db:
            raise HTTPException(status_code=404, detail="Хобби не найдено")
        return hobby_in_db

    @classmethod
    async def all_hobbies(cls):
        async with async_session_maker() as session:
            hobbies_execute = await session.execute(select(Hobby))
            return hobbies_execute.scalars().all()

    @classmethod
    async def add_hobby(cls, hobby_data: AddHobby):
        async with async_session_maker() as session:

            check = await session.execute(select(Hobby).filter_by(hobby_name=hobby_data.hobby_name))
            if check.scalars().one_or_none():
                raise HTTPException(status_code=404, detail="Хобби уже существует")

            hobby = Hobby(**hobby_data.model_dump())
            session.add(hobby)
            await session.flush() 
            await session.commit()
            await session.refresh(hobby)
            return hobby

    @classmethod
    async def remove_hobby(cls, id: int):
        async with async_session_maker() as session:
            hobby = await cls.hobby_by_id(session, id)
            await session.delete(hobby)
            await session.commit()
            return {"result": "Хобби удалено"}


        

