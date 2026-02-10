from fastapi import APIRouter, Response, Depends
#from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.schemas import UserRegistrationScheme

router = APIRouter(prefix='/user', tags=['User'])

@router.post("/registration")
async def register_user(user: UserRegistrationScheme) -> UserRegistrationScheme:
    return {'result': 'ok'}