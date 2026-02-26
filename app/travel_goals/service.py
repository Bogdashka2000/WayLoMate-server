from app.database import async_session_maker
from sqlalchemy import select
from app.travel_goals.models import TravelGoal
from sqlalchemy.ext.asyncio import AsyncSession
from app.travel_goals.schemas import AddGoal
from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException


class GoalService:
    
    @classmethod
    async def goal_by_id(cls, session: AsyncSession, goal_id: int):  
        check = await session.execute(select(TravelGoal).filter_by(id=goal_id))
        goal_in_db = check.scalars().one_or_none()
        if not goal_in_db:
            raise HTTPException(status_code=404, detail="Цель путeшествия не найдена")
        return goal_in_db

    @classmethod
    async def all_goals(cls):
        async with async_session_maker() as session:
            goal_execute = await session.execute(select(TravelGoal))
            return goal_execute.scalars().all()

    @classmethod
    async def add_goal(cls, goal_data: AddGoal):
        async with async_session_maker() as session:
            
            check = await session.execute(select(TravelGoal).filter_by(travel_goal_name=goal_data.travel_goal_name))
            if check.scalars().one_or_none():
                raise HTTPException(status_code=404, detail="Цель путeшествия уже существует")


            goal = TravelGoal(**goal_data.model_dump())
            session.add(goal)
            await session.flush() 
            await session.commit()
            await session.refresh(goal)
            return goal

    @classmethod
    async def remove_goal(cls, id: int):
        async with async_session_maker() as session:
            goal = await cls.goal_by_id(session, id)
            await session.delete(goal)
            await session.commit()
            return {"result": "Цель путшествия удалена"}


        

