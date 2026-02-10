from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.users.route import router as users_route
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), 'static')

@app.get('/')
def home_page():
    return {'test': 'test'}

app.include_router(users_route)