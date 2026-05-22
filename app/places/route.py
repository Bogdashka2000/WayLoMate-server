from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.places.service import PlaceService
from app.places.schemas import PlaceInfo, AddPlace
from app.users.schemas import UserAvaibleInfo
from app.users.auth import get_user_by_token
from typing import List, Optional
import uuid
import shutil
import os
from pathlib import Path

router = APIRouter(prefix='/places', tags=['Places'])

UPLOAD_DIR = Path("app/static/uploads/places")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/", response_model=List[PlaceInfo])
async def all_places():
    return await PlaceService.all_places()

@router.get("/{id}", response_model=PlaceInfo)
async def get_place(id: int):
    place = await PlaceService.get_place_by_id(id)
    if not place:
        raise HTTPException(status_code=404, detail="Место не найдено")
    return place

@router.post("/add", response_model=PlaceInfo)
async def create_place(
    name: str = Form(..., description="Название места"),
    description: str = Form(..., description="Описание места"),
    location: Optional[str] = Form(None, description="Расположение"),
    category: Optional[str] = Form(None, description="Категория"),
    image: UploadFile = File(..., description="Изображение места"),
    user: UserAvaibleInfo = Depends(get_user_by_token)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Допускаются только изображения (JPEG, PNG, WEBP)")
        
    ext = image.filename.rsplit(".", 1)[-1].lower() if "." in (image.filename or "") else "jpg"
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    image_url = f"/static/uploads/places/{unique_filename}"
    
    place_data = AddPlace(
        name=name,
        description=description,
        image_url=image_url,
        location=location,
        category=category
    )
    
    return await PlaceService.add_place(user_id=user[0].id, place_data=place_data)

@router.put("/update/{id}", response_model=PlaceInfo)
async def update_place(
    id: int,
    name: str = Form(...),
    description: str = Form(...),
    location: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    user: UserAvaibleInfo = Depends(get_user_by_token)
):
    place = await PlaceService.get_place_by_id(id)
    if not place:
        raise HTTPException(status_code=404, detail="Место не найдено")
        
    if place.user_id != user[0].id:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование")
        
    image_url = place.image_url
    
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Допускаются только изображения")
            
        old_filename = place.image_url.split("/")[-1]
        old_path = UPLOAD_DIR / old_filename
        if old_path.exists():
            os.remove(old_path)
            
        ext = image.filename.rsplit(".", 1)[-1].lower() if "." in (image.filename or "") else "jpg"
        unique_filename = f"{uuid.uuid4()}.{ext}"
        file_path = UPLOAD_DIR / unique_filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/uploads/places/{unique_filename}"
        
    place_data = AddPlace(
        name=name,
        description=description,
        image_url=image_url,
        location=location,
        category=category
    )
    
    return await PlaceService.update_place(id, place_data)

@router.delete("/remove/{id}")
async def remove_place(id: int, user: UserAvaibleInfo = Depends(get_user_by_token)):
    place = await PlaceService.get_place_by_id(id)
    if not place:
        raise HTTPException(status_code=404, detail="Место не найдено")
        
    if place.user_id != user[0].id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление")
        
    filename = place.image_url.split("/")[-1]
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        os.remove(file_path)
        
    return await PlaceService.remove_place(id)