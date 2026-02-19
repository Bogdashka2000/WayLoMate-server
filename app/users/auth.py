from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.configurator import get_auth_data
from app.users.service import UserService
from fastapi import Request, HTTPException, status, Depends

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_password(password: str) -> str:
    return hash_context.hash(password)

def verify_password(res_pass: str, hash_pass: str) -> bool:
    return hash_context.verify(res_pass, hash_pass)

def create_token(data: dict) -> str:
    data_cpy = data.copy()
    time = datetime.now(timezone.utc) + timedelta(days=90)
    data_cpy.update({"exp":time})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(data_cpy, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

def get_token(request: Request):
    token = request.cookies.get("user_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не найден')
    return token

async def get_user_by_token(token: srt = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data["algorithm"]])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неправильный токен')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='ID отсутствует')
    
    user = await UserService.find_all_validation_users(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователя не существует')
    return user