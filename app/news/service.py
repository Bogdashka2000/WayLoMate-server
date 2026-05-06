from app.database import async_session_maker
from sqlalchemy import select, delete
from app.news.models import News
from sqlalchemy.ext.asyncio import AsyncSession
from app.news.schemas import NewsInfo, AddNews
from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException

class NewsService:

    @classmethod
    async def all_news(cls):
        async with async_session_maker() as session:
            news_execute = await session.execute(select(News))
            return news_execute.scalars().all()

    @classmethod
    async def add_news(cls, user_id: int, news_data: AddNews):
        async with async_session_maker() as session:
            news = News(**news_data.model_dump(), user_id=user_id)
            
            session.add(news)
            await session.flush() 
            await session.commit()
            await session.refresh(news)
            return news
   
    @classmethod
    async def remove_news(cls, id: int):
        async with async_session_maker() as session: 
            result = await session.execute(
                delete(News).where(News.id == id)
            )
            await session.commit()
            
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Новость не найдена")
                
            return {"result": "Новость удалена"}  