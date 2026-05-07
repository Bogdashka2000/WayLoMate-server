from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.users.schemas import UserAvaibleInfo
from app.users.auth import get_admin_by_token, get_user_by_token
from app.admin.service import AdminService
from typing import List

router = APIRouter(prefix='/admin', tags=['Admin Preference'])

@router.delete("/remove/user/{id}")
async def remove_user(id: int, is_admin: bool = Depends(get_admin_by_token)):
    result = await AdminService.remove_user(id)
    return result

@router.delete("/remove/post/{id}")
async def remove_post(id: int, is_admin: bool = Depends(get_admin_by_token)):
    result = await AdminService.remove_post(id)
    return result

@router.delete("/remove/comment/{id}")
async def remove_comment(id: int, is_admin: bool = Depends(get_admin_by_token)):
    result = await AdminService.remove_comment(id)
    return result

