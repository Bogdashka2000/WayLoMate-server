from app.database import async_session_maker
from sqlalchemy import select
from app.posts.models import Post
from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.schemas import AddPost
from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException


class PostService:
    
    @classmethod
    async def session_post_by_id(cls, post_id: int): 
        async with async_session_maker() as session:
            return await cls.post_by_id(session=session, post_id=post_id)

    @classmethod
    async def post_by_id(cls, session: AsyncSession, post_id: int):  
        check = await session.execute(select(Post).filter_by(id=post_id))
        post_in_db = check.scalars().one_or_none()
        if not post_in_db:
            raise HTTPException(status_code=404, detail="Пост не найден")
        return post_in_db

    @classmethod
    async def post_by_user_id(cls, user_id: int):  
        async with async_session_maker() as session:
            check = await session.execute(select(Post).filter_by(user_id=user_id))
            post_in_db = check.scalars().all()
            if not post_in_db:
                raise HTTPException(status_code=404, detail="Пост не найден")
            return post_in_db

    @classmethod
    async def all_posts(cls):
        async with async_session_maker() as session:
            post_execute = await session.execute(select(Post))
            return post_execute.scalars().all()

    @classmethod
    async def add_post(cls, user_id: int, post_data: AddPost):
        async with async_session_maker() as session:


            post = Post(**post_data.model_dump())

            post.user_id = user_id

            session.add(post)
            await session.flush() 
            await session.commit()
            await session.refresh(post)
            return post

    @classmethod
    async def remove_post(cls, id: int, user_id: int):
        async with async_session_maker() as session:
            post = await cls.post_by_id(session, id)

            if(post.user_id != user_id):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Только пользователь может удалить свой пост')
            
            await session.delete(post)
            await session.commit()
            return {"result": "Пост удалён"}


        

