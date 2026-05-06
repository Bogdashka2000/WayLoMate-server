from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.users.schemas import UserAvaibleInfo
from app.users.auth import get_admin_by_token
from typing import List
from starlette.websockets import WebSocket, WebSocketDisconnect
from app.chat.auth import get_user_by_token_ws
from app.chat.connection_manager import manager
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix='/chat', tags=['Chat Preference'])


@router.websocket("/connect_to_chat")
async def chat_endpoint(websocket: WebSocket, user: UserAvaibleInfo = Depends(get_user_by_token_ws)):
    logger.info(f"WebSocket connected: user_id={user.id} ({user.first_name} {user.last_name})")
    await manager.connect(websocket, user.id)
    try:
        while True:
            data = await websocket.receive_json()
            client_msg = data.get("message", "").strip()
            if not client_msg: continue

            payload = {
                "user": user.model_dump(mode="json"),
                "message": client_msg
            }
            await manager.broadcast(payload)
    except WebSocketDisconnect:
        manager.disconnect(user.id)
        logger.info(f"🔌 WebSocket disconnected: user_id={user.id}")
    except Exception as e:
        manager.disconnect(user.id)
        logger.error(f"WS Error: {e}")
        await websocket.close(code=1011, reason="Internal server error")