import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, Avatar
from app.schemas import ProfileUpdate, PasswordChange, AccountDelete
from app.dependencies import get_current_active_user
from app.utils import verify_password, hash_password

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/avatars")
async def get_avatars(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Avatar))
    avatars = q.scalars().all()
    return [{"id": a.id, "image_url": a.image_url, "category": a.category} for a in avatars]

@router.put("/")
async def update_profile(
    data: ProfileUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if data.full_name is not None:
        current_user.full_name = data.full_name
    if data.gender is not None:
        current_user.gender = data.gender
    if data.gender_preference is not None:
        current_user.gender_preference = data.gender_preference
    if data.avatar_id is not None:
        current_user.avatar_id = data.avatar_id
    if data.customizations is not None:
        current_user.customizations = data.customizations
    if data.interests is not None:
        current_user.interests = data.interests
    
    await db.commit()
    return {"message": "Profile updated successfully"}


@router.put("/password")
async def change_password(
    data: PasswordChange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect current password")
    
    current_user.hashed_password = hash_password(data.new_password)
    await db.commit()
    return {"message": "Password updated successfully"}

@router.post("/account/delete")
async def delete_account(
    data: AccountDelete,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    # Soft delete: wipe personal data and deactivate
    current_user.is_active = False
    current_user.email = f"deleted_{current_user.id}@deleted.com"
    current_user.hashed_password = ""
    await db.commit()
    return {"message": "Account deleted successfully"}

@router.get("/me")
async def get_my_profile(current_user: User = Depends(get_current_active_user)):
    age = None
    if current_user.date_of_birth:
        today = datetime.utcnow()
        age = today.year - current_user.date_of_birth.year - ((today.month, today.day) < (current_user.date_of_birth.month, current_user.date_of_birth.day))
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "gender": current_user.gender,
        "gender_preference": current_user.gender_preference,
        "customizations": current_user.customizations,
        "profile_picture_url": current_user.profile_picture_url,
        "age": age,
        "rating": current_user.rating,
        "interests": current_user.interests
    }

@router.post("/picture/upload")
async def upload_profile_picture(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    extension = file.filename.split(".")[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, and WEBP allowed.")
        
    filename = f"{current_user.id}_avatar.{extension}"
    file_path = os.path.join("static", "uploads", filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
        
    current_user.profile_picture_url = f"/static/uploads/{filename}"
    await db.commit()
    
    return {
        "message": "Profile picture uploaded successfully", 
        "url": current_user.profile_picture_url
    }
