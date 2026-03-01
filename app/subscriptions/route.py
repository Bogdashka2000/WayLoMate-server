from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.subscriptions.service import SubscriptionService
from app.subscriptions.schemas import ToggleResult, AddSub
from app.users.schemas import UserAvaibleInfo
from app.users.auth import get_user_by_token
from typing import List

router = APIRouter(prefix='/subscription', tags=['Subscription Preference'])

@router.post("/toggle",  response_model=ToggleResult)
async def toggle_like(following: AddSub, user: user = Depends(get_user_by_token)):
    toggle = await SubscriptionService.toggle_sub(follower_id = user[0].id, following_id = following.user_id)
    return toggle

@router.get("/followers/{id}", response_model=List[UserAvaibleInfo])
async def get_followers(id: int):
    followers = await SubscriptionService.subscribers_by_user(id)
    return followers

@router.get("/followed/{id}", response_model=List[UserAvaibleInfo])
async def get_followers(id: int):
    followed = await SubscriptionService.subscribes_by_user(id)
    return followed