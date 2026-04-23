from app.database import async_session_maker
from sqlalchemy import select
from app.comments.models import Comment
from app.posts.service import PostService
from sqlalchemy.ext.asyncio import AsyncSession
from app.comments.schemas import AddComment
from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException


class CommentService:
    
    @classmethod
    async def session_comment_by_id(cls, comment_id: int): 
        async with async_session_maker() as session:
            return await cls.comment_by_id(session=session, comment_id=comment_id)

    @classmethod
    async def comment_by_id(cls, session: AsyncSession, comment_id: int):  
        check = await session.execute(select(Comment).filter_by(id=comment_id))
        comment_in_db = check.scalars().one_or_none()
        if not comment_in_db:
            raise HTTPException(status_code=404, detail="Комментарий не найден")
        return comment_in_db

    @classmethod
    async def comment_by_post_id(cls, post_id: int):  
        async with async_session_maker() as session:
            check = await session.execute(select(Comment).filter_by(post_id=post_id))
            comment_in_db = check.scalars().all()
            if not comment_in_db:
                raise HTTPException(status_code=404, detail="Комментарий не найден")
            return comment_in_db

    @classmethod
    async def all_comments(cls):
        async with async_session_maker() as session:
            comment_execute = await session.execute(select(Comment))
            return comment_execute.scalars().all()

    @classmethod
    async def add_comment(cls, user_id: int, comment_data: AddComment):
        async with async_session_maker() as session:
            post = await PostService.session_post_by_id(
    user_id=user_id, 
    post_id=comment_data.post_id
)

            if post is None:
                raise HTTPException(status_code=404, detail="Пост не найден")

            comment = Comment(**comment_data.model_dump())
            comment.user_id = user_id
            session.add(comment)
            await session.flush() 
            await session.commit()
            return comment

    @classmethod
    async def remove_comment(cls, id: int, user_id: int):
        async with async_session_maker() as session:
            comment = await cls.comment_by_id(session, id)

            if(comment.user_id != user_id):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Только пользователь может удалить свой комментарий')
            
            await session.delete(comment)
            await session.commit()
            return {"result": "Комментарий удалён"}


        

