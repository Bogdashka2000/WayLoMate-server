# app/chat/auth.py
from fastapi import WebSocket, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timezone
import logging

from app.configurator import get_auth_data
from app.users.service import UserService
from app.users.schemas import UserAvaibleInfo

logger = logging.getLogger(__name__)

async def get_user_by_token_ws(websocket: WebSocket) -> UserAvaibleInfo:
    token = websocket.query_params.get("token") or websocket.cookies.get("user_token")
    
    if not token:
        logger.warning("WS Auth: Missing token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Токен не найден"
        )

    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, 
            auth_data["secret_key"], 
            algorithms=[auth_data["algorithm"]]
        )
    except JWTError as e:
        logger.error(f"WS Auth: JWT decode error -> {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Неправильный токен"
        )
    expire = payload.get("exp")
    if expire is None:
        logger.error("WS Auth: Missing 'exp' claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Невалидный токен"
        )
        
    expire_time = datetime.fromtimestamp(float(expire), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        logger.warning("WS Auth: Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Токен истек"
        )

    user_id = payload.get("sub")
    if not user_id:
        logger.error("WS Auth: Missing 'sub' claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="ID отсутствует"
        )

    try:
        user_list = await UserService.find_all_validation_users(id=int(user_id))
        
        if not user_list:
            logger.warning(f"WS Auth: User {user_id} not found in DB")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Пользователь не найден"
            )
            
        return UserAvaibleInfo.model_validate(user_list[0])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"WS Auth: Unexpected error -> {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Ошибка авторизации"
        )