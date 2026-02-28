from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.likes.models import Like
from app.posts.models import Post
from app.posts.service import PostService
from fastapi import HTTPException, status

class LikeService:
    
    @classmethod
    async def like_total(cls, session: AsyncSession, post_id: int):
            count_res = await session.execute(
                select(func.count(Like.id)).where(Like.post_id == post_id)
            )
            return count_res.scalar() or 0

    @classmethod
    async def toggle_like(cls, user_id: int, post_id: int):
        async with async_session_maker() as session:
            
            is_liked = False
            action = "unliked"

            post = await PostService.post_by_id(session=session, post_id=post_id)
            
            if not post:
                raise HTTPException(status_code=404, detail="Пост не найден")

            search_like = await session.execute(select(Like).where(
                Like.user_id == user_id,
                Like.post_id == post_id
            ))

            like = search_like.scalar_one_or_none()

            if like:
                await session.delete(like)
                action = "unliked"
                is_liked = False
            else:
                new_like = Like(user_id=user_id, post_id=post_id)
                session.add(new_like)
                action = "liked"
                is_liked = True

            await session.commit()

            total_likes = await cls.like_total(session=session, post_id=post_id)

            return {
                "action": action,
                "is_liked": is_liked,
                "total_likes": total_likes
            }

