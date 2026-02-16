from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.configurator import get_auth_data
from app.users.service import UserService

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_password(password: str) -> str:
    return hash_context.hash(password)

def verify_password(res_pass: str, hash_pass: str) -> bool:
    return hash_context.verify(res_pass, hash_pass)

def create_token(data: dict) -> str:
    data_cpy = data.copy()
    time = datetime.now(timezone.utc) + timedelta(days=90)
    data_cpy.update({"exp":time})
    auth_data = get_auth_data
    encode_jwt = jwt_encode(data_cpy, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt