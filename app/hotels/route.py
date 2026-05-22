from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.hotels.service import HotelService
from app.hotels.schemas import HotelInfo, AddHotel
from app.users.schemas import UserAvaibleInfo
from app.users.auth import get_user_by_token
from typing import List, Optional
import uuid
import shutil
import os
from pathlib import Path

router = APIRouter(prefix='/hotels', tags=['Hotels'])

UPLOAD_DIR = Path("app/static/uploads/hotels")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/", response_model=List[HotelInfo])
async def all_hotels():
    return await HotelService.all_hotels()

@router.get("/{id}", response_model=HotelInfo)
async def get_hotel(id: int):
    hotel = await HotelService.get_hotel_by_id(id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return hotel

@router.post("/add", response_model=HotelInfo)
async def create_hotel(
    name: str = Form(..., description="Название отеля"),
    description: str = Form(..., description="Описание отеля"),
    location: Optional[str] = Form(None, description="Расположение"),
    rating: Optional[float] = Form(None, description="Рейтинг"),
    image: UploadFile = File(..., description="Изображение отеля"),
    user: UserAvaibleInfo = Depends(get_user_by_token)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Допускаются только изображения (JPEG, PNG, WEBP)")
        
    ext = image.filename.rsplit(".", 1)[-1].lower() if "." in (image.filename or "") else "jpg"
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    image_url = f"/static/uploads/hotels/{unique_filename}"
    
    hotel_data = AddHotel(
        name=name,
        description=description,
        image_url=image_url,
        location=location,
        rating=rating
    )
    
    return await HotelService.add_hotel(user_id=user[0].id, hotel_data=hotel_data)

@router.put("/update/{id}", response_model=HotelInfo)
async def update_hotel(
    id: int,
    name: str = Form(...),
    description: str = Form(...),
    location: Optional[str] = Form(None),
    rating: Optional[float] = Form(None),
    image: Optional[UploadFile] = File(None),
    user: UserAvaibleInfo = Depends(get_user_by_token)
):
    hotel = await HotelService.get_hotel_by_id(id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
        
    if hotel.user_id != user[0].id:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование")
        
    image_url = hotel.image_url
    
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Допускаются только изображения")
            
        old_filename = hotel.image_url.split("/")[-1]
        old_path = UPLOAD_DIR / old_filename
        if old_path.exists():
            os.remove(old_path)
            
        ext = image.filename.rsplit(".", 1)[-1].lower() if "." in (image.filename or "") else "jpg"
        unique_filename = f"{uuid.uuid4()}.{ext}"
        file_path = UPLOAD_DIR / unique_filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/uploads/hotels/{unique_filename}"
        
    hotel_data = AddHotel(
        name=name,
        description=description,
        image_url=image_url,
        location=location,
        rating=rating
    )
    
    return await HotelService.update_hotel(id, hotel_data)

@router.delete("/remove/{id}")
async def remove_hotel(id: int, user: UserAvaibleInfo = Depends(get_user_by_token)):
    hotel = await HotelService.get_hotel_by_id(id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
        
    if hotel.user_id != user[0].id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление")
        
    filename = hotel.image_url.split("/")[-1]
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        os.remove(file_path)
        
    return await HotelService.remove_hotel(id)