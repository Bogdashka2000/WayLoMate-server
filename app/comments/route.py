from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.comments.service import CommentService
from app.comments.schemas import CommentInfo, AddComment
from app.users.auth import get_user_by_token
from typing import List

router = APIRouter(prefix='/comment', tags=['Comment Preference'])

@router.get("/",  response_model=List[CommentInfo])
async def all_comments():
    comment_list = await CommentService.all_comments()
    return comment_list

@router.get("/{id}", response_model=CommentInfo)
async def comment_by_id(id: int):
    comment = await CommentService.session_comment_by_id(id)
    return comment

@router.get("/by_post/{post_id}", response_model=List[CommentInfo])
async def comment_by_post_id(post_id: int):
    comments = await CommentService.comment_by_post_id(post_id=post_id)
    return comments

@router.post("/add", response_model=CommentInfo)
async def create_new_comment(comment_data: AddComment, user: user = Depends(get_user_by_token)):
    comment = await CommentService.add_comment(user_id=user[0].id, comment_data=comment_data)
    return comment

@router.delete("/remove/{id}")
async def remove_post(id: int, user: user = Depends(get_user_by_token)):
    comment = await PostService.remove_comment(id, user[0].id)
    return comment

