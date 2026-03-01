from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.subscriptions.models import Subscription
from app.users.models import User
from fastapi import HTTPException, status

class SubscriptionService:

    @classmethod
    async def toggle_sub(cls, follower_id: int, following_id: int):
        async with async_session_maker() as session:
            action = ""
            is_subscribed = False


            if follower_id == following_id:
                raise HTTPException(status_code=400, detail="Нельзя подписаться на самого себя")
            

            user_check = await session.execute(
                select(User).where(User.id == following_id)
            )

            if not user_check.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            sub_check = await session.execute(
                select(Subscription).where(
                    Subscription.user_id == follower_id,       
                    Subscription.subscriber_to_id == following_id 
                )
            )

            subs_in_db = sub_check.scalar_one_or_none()

            if subs_in_db:
                await session.delete(subs_in_db)
                action = "unsubscribed"
                is_subscribed = False
            else:
                new_sub = Subscription(
                    user_id=follower_id, 
                    subscriber_to_id=following_id
                )
                session.add(new_sub)
                action = "subscribed"
                is_subscribed = True
            
            await session.commit()

            return {
                "action": action,
                "is_subscribed": is_subscribed,
            }

    @classmethod
    async def subscribers_by_user(cls, user_id):
        async with async_session_maker() as session:
            user_check = await session.execute(
                    select(User).where(User.id == user_id)
                )

            if not user_check.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            sub_check = await session.execute(
                select(Subscription).where(
                    Subscription.subscriber_to_id == user_id,
                    )
                )
            subscriptions = sub_check.scalars().all()
            follower_ids = [sub.user_id for sub in subscriptions]
            followers = await session.execute(select(User).where(User.id.in_(follower_ids)))
            return followers.scalars().all()

    @classmethod
    async def subscribes_by_user(cls, user_id):
        async with async_session_maker() as session:
            user_check = await session.execute(
                    select(User).where(User.id == user_id)
                )

            if not user_check.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            sub_check = await session.execute(
                select(Subscription).where(
                    Subscription.user_id == user_id,
                    )
                )
            subscriptions = sub_check.scalars().all()
            following_ids = [sub.subscriber_to_id for sub in subscriptions]
            following = await session.execute(select(User).where(User.id.in_(following_ids)))
            return following.scalars().all()
        