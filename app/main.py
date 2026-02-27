from fastapi import FastAPI
import os
from starlette.requests import Request
from starlette.responses import RedirectResponse, FileResponse
from app.users.route import router as users_route
from app.hobbies.route import router as hobbies_route
from app.languages.route import router as languages_route
from app.travel_goals.route import router as goals_route
from app.posts.route import router as post_router

from fastapi.staticfiles import StaticFiles

app = FastAPI()



STATIC_DIR_AVATAR = "app/static/avatar_images"
STATIC_DIR_HEADER = "app/static/header_images"
STATIC_DIR_POST_PICTURES = "app/static/post_pictures"

os.makedirs(STATIC_DIR_AVATAR, exist_ok=True)
os.makedirs(STATIC_DIR_HEADER, exist_ok=True)
os.makedirs(STATIC_DIR_POST_PICTURES, exist_ok=True)


app.mount('/static', StaticFiles(directory='app/static'), 'static')

@app.get("/favicon.ico")
def mainpage():
    return FileResponse("favicon.ico")

app.include_router(users_route)
app.include_router(hobbies_route)
app.include_router(languages_route)
app.include_router(goals_route)
app.include_router(post_router)