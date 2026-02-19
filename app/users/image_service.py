from fastapi import UploadFile, File
from app.configurator import get_static_path
import uuid
import os
import shutil


class UserImageService:

    @classmethod
    async def save_image(cls, file: File, env_static_file_path: str):
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл должен быть изображением (jpg, png, gif и т.д.)")
    
        file_ext = os.path.splitext(file.filename)[1].lower()
        data = get_static_path()

        file_path = os.path.join(data[env_static_file_path], f'{uuid.uuid4()}{file_ext}')
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path