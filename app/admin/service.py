from app.comments.models import Comment
from app.posts.models import Post
from app.users.models import User
from app.database import async_session_maker  
from sqlalchemy import select
from fastapi import HTTPException, status

class AdminService:

    @classmethod
    async def remove_user(cls, user_id: int):
        async with async_session_maker() as session:   
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

            await session.delete(user)
            await session.commit()
            return {"status": "Пользователь удалён"}

    @classmethod
    async def remove_post(cls, post_id: int):
        async with async_session_maker() as session:
            result = await session.execute(select(Post).filter_by(id=post_id))
            post = result.scalars().first()

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пост не найден")

            await session.delete(post)
            await session.commit()
            return {"status": "Пост удалён"}

    @classmethod
    async def remove_comment(cls, comment_id: int):
        async with async_session_maker() as session:
            result = await session.execute(select(Comment).filter_by(id=comment_id))
            comment = result.scalars().first()
            
            if not comment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комментарий не найден")

            await session.delete(comment)
            await session.commit()
            return {"status": "Комментарий удалён"}