from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.posts.service import PostService
from app.posts.schemas import PostInfo, AddPost 
from app.users.auth import get_user_by_token
from typing import List

router = APIRouter(prefix='/post', tags=['Post Preference'])

@router.get("/",  response_model=List[PostInfo])
async def all_posts():
    post_list = await PostService.all_posts()
    return post_list

@router.get("/{id}", response_model=PostInfo)
async def post_by_id(id: int):
    post = await PostService.session_post_by_id(id)
    return post

@router.get("/by_user/{user_id}", response_model=List[PostInfo])
async def post_by_user_id(user_id: int):
    posts = await PostService.post_by_user_id(user_id)
    return posts

@router.post("/add", response_model=PostInfo)
async def create_new_post(post_data: AddPost, user: user = Depends(get_user_by_token)):
    post = await PostService.add_post(user_id=user[0].id, post_data=post_data)
    return post

@router.delete("/remove/{id}")
async def remove_post(id: int, user: user = Depends(get_user_by_token)):
    post = await PostService.remove_post(id, user[0].id)
    return post

