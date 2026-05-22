from app.database import async_session_maker
from sqlalchemy import select, delete
from app.places.models import Place
from sqlalchemy.ext.asyncio import AsyncSession
from app.places.schemas import PlaceInfo, AddPlace
from fastapi import HTTPException


class PlaceService:

    @classmethod
    async def all_places(cls):
        async with async_session_maker() as session:
            places_execute = await session.execute(select(Place))
            return places_execute.scalars().all()

    @classmethod
    async def get_place_by_id(cls, place_id: int):
        async with async_session_maker() as session:
            place = await session.get(Place, place_id)
            return place

    @classmethod
    async def add_place(cls, user_id: int, place_data: AddPlace):
        async with async_session_maker() as session:
            place = Place(**place_data.model_dump(), user_id=user_id)
            
            session.add(place)
            await session.flush() 
            await session.commit()
            await session.refresh(place)
            return place
   
    @classmethod
    async def update_place(cls, place_id: int, place_data: AddPlace):
        async with async_session_maker() as session:
            place = await session.get(Place, place_id)
            if not place:
                raise HTTPException(status_code=404, detail="Место не найдено")
            
            for field, value in place_data.model_dump(exclude_unset=True).items():
                setattr(place, field, value)
            
            await session.commit()
            await session.refresh(place)
            return place

    @classmethod
    async def remove_place(cls, id: int):
        async with async_session_maker() as session: 
            result = await session.execute(
                delete(Place).where(Place.id == id)
            )
            await session.commit()
            
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Место не найдено")
                
            return {"result": "Место удалено"}