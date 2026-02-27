from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.travel_goals.service import GoalService
from app.travel_goals.schemas import GoalInfo, AddGoal
from app.users.auth import get_admin_by_token
from typing import List

router = APIRouter(prefix='/goal', tags=['Travel Goal Preference'])

@router.get("/", response_model=List[GoalInfo])
async def all_goals():
    goals = await GoalService.all_goals()
    return goals

@router.post("/add", response_model=GoalInfo)
async def create_new_goal(goal: AddGoal, is_admin: bool = Depends(get_admin_by_token)):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У пользователя нет прав администратора')
    goal = await GoalService.add_goal(goal)
    return goal

@router.delete("/remove/{id}")
async def remove_goal(id: int, is_admin: bool = Depends(get_admin_by_token)):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='У пользователя нет прав администратора')
    goal = await GoalService.remove_goal(id)
    return goal