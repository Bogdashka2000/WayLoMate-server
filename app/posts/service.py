from app.database import async_session_maker
from sqlalchemy import select, func
from app.posts.models import Post
from app.comments.models import Comment
from app.likes.models import Like
from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.schemas import AddPost
from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException


class PostService:
    
    @classmethod
    async def is_liked_by_user(cls, session: AsyncSession, user_id: int, post_id: int) -> bool:
        result = await session.execute(
            select(Like).where(
                Like.user_id == user_id,
                Like.post_id == post_id
        ))
        like = result.scalar_one_or_none()
        
        return like is not None


    @classmethod
    async def post_by_id(cls, session: AsyncSession, post_id: int):  
        check = await session.execute(select(Post).filter_by(id=post_id))
        post_in_db = check.scalars().one_or_none()
        if not post_in_db:
            raise HTTPException(status_code=404, detail="Пост не найден")
        return post_in_db

    @classmethod
    async def session_post_by_id(cls, user_id:int, post_id: int): 
        async with async_session_maker() as session:
            post = await cls.post_by_id(session=session, post_id=post_id)
            comm = await session.execute(select(func.count(Comment.id)).where(Comment.post_id == post_id))
            comment_count = comm.scalar() or 0

            like = await session.execute(select(func.count(Like.id)).where(Like.post_id == post_id))
            like_count = like.scalar() or 0

            is_liked = False
            if user_id:
                is_liked = await cls.is_liked_by_user(session, user_id, post_id)

            return {
                "id": post.id,
                "text": post.text,
                "image_url": post.image_url,
                "user_id": post.user_id,
                "created_at": post.created_at,
                "like_count": like_count,
                "comment_count": comment_count,
                "is_liked": is_liked
            }

    @classmethod
    async def post_by_user_id(cls, current_user_id: int, user_id: int):  
        async with async_session_maker() as session:
            check = await session.execute(select(Post).filter_by(user_id=user_id))
            post_in_db = check.scalars().all()
            if not post_in_db:
                raise HTTPException(status_code=404, detail="Пост не найден")
            response_list = []
            for post in post_in_db:
                comm_count = (await session.execute(select(func.count(Comment.id)).where(Comment.post_id == post.id))).scalar() or 0
                like_count = (await session.execute(select(func.count(Like.id)).where(Like.post_id == post.id))).scalar() or 0    
                is_liked = False
                if user_id:
                    is_liked = await cls.is_liked_by_user(session, post.id, current_user_id)

                response_list.append({
                    "id": post.id,
                    "text": post.text,
                    "image_url": post.image_url,
                    "user_id": post.user_id,
                    "created_at": post.created_at,
                    "like_count": like_count,
                    "comment_count": comm_count,
                    "is_liked": is_liked
                })
            return response_list

    @classmethod
    async def all_posts(cls, current_user_id):
        async with async_session_maker() as session:
            post_execute = await session.execute(select(Post))
            posts = post_execute.scalars().all()

            response_list = []
            for post in posts:
                stmt_comm = select(func.count(Comment.id)).where(Comment.post_id == post.id)
                comm_count = (await session.execute(stmt_comm)).scalar() or 0

                stmt_like = select(func.count(Like.id)).where(Like.post_id == post.id)
                like_count = (await session.execute(stmt_like)).scalar() or 0
                
                is_liked = False
                if current_user_id:
                    is_liked = await cls.is_liked_by_user(session, current_user_id,  post.id)

                response_list.append({
                    "id": post.id,
                    "text": post.text,
                    "image_url": post.image_url,
                    "user_id": post.user_id,
                    "created_at": post.created_at,
                    "like_count": like_count,
                    "comment_count": comm_count,
                    "is_liked": is_liked
                })
            
            return response_list

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


        

