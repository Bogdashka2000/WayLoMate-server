from app.database import async_session_maker
from sqlalchemy import select, delete
from app.hotels.models import Hotel
from sqlalchemy.ext.asyncio import AsyncSession
from app.hotels.schemas import HotelInfo, AddHotel
from fastapi import HTTPException


class HotelService:

    @classmethod
    async def all_hotels(cls):
        async with async_session_maker() as session:
            hotels_execute = await session.execute(select(Hotel))
            return hotels_execute.scalars().all()

    @classmethod
    async def get_hotel_by_id(cls, hotel_id: int):
        async with async_session_maker() as session:
            hotel = await session.get(Hotel, hotel_id)
            return hotel

    @classmethod
    async def add_hotel(cls, user_id: int, hotel_data: AddHotel):
        async with async_session_maker() as session:
            hotel = Hotel(**hotel_data.model_dump(), user_id=user_id)
            
            session.add(hotel)
            await session.flush() 
            await session.commit()
            await session.refresh(hotel)
            return hotel
   
    @classmethod
    async def update_hotel(cls, hotel_id: int, hotel_data: AddHotel):
        async with async_session_maker() as session:
            hotel = await session.get(Hotel, hotel_id)
            if not hotel:
                raise HTTPException(status_code=404, detail="Отель не найден")
            
            for field, value in hotel_data.model_dump(exclude_unset=True).items():
                setattr(hotel, field, value)
            
            await session.commit()
            await session.refresh(hotel)
            return hotel

    @classmethod
    async def remove_hotel(cls, id: int):
        async with async_session_maker() as session: 
            result = await session.execute(
                delete(Hotel).where(Hotel.id == id)
            )
            await session.commit()
            
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Отель не найден")
                
            return {"result": "Отель удален"}