from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.likes.service import LikeService
from app.likes.schemas import LikeInfo, AddLike
from app.users.auth import get_user_by_token
from typing import List

router = APIRouter(prefix='/like', tags=['Like Preference'])

@router.post("/toggle",  response_model=LikeInfo)
async def toggle_like(like: AddLike, user: user = Depends(get_user_by_token)):
    toggle = await LikeService.toggle_like(user_id = user[0].id, post_id = like.post_id)
    return toggle

