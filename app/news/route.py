from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.news.service import NewsService
from app.news.schemas import NewsInfo, AddNews
from app.users.schemas import UserAvaibleInfo
from app.users.auth import get_admin_by_token, get_user_by_token
from typing import List

router = APIRouter(prefix='/news', tags=['News Preference'])

@router.get("/",  response_model=List[NewsInfo])
async def all_news():
    news_list = await NewsService.all_news()
    return news_list

@router.post("/add", response_model=NewsInfo)
async def create_new_news(news_data: AddNews, is_admin: bool = Depends(get_admin_by_token), user: UserAvaibleInfo = Depends(get_user_by_token)):
    news = await NewsService.add_news(user_id=user[0].id, news_data=news_data)
    return news

@router.delete("/remove/{id}")
async def remove_post(id: int, is_admin: bool = Depends(get_admin_by_token), user: UserAvaibleInfo = Depends(get_user_by_token)):
    news = await NewsService.remove_news(id)
    return news

