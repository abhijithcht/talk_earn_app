from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import random
from app.schemas import UserCreate, Token, VerifyEmailRequest
from app.models import User, Wallet
from app.utils import hash_password, verify_password
from app.database import get_db
from app.auth import create_access_token
from app.services.email_service import send_otp_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.email == user_in.email))
    existing = q.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    otp = str(random.randint(100000, 999999))
    user = User(
        email=user_in.email, 
        hashed_password=hash_password(user_in.password), 
        gender=user_in.gender,
        otp_code=otp
    )
    db.add(user)
    await db.flush()
    wallet = Wallet(user_id=user.id, balance=0)
    db.add(wallet)
    await db.commit()
    
    await send_otp_email(user.email, otp)
    return {"message": "registered. Please verify your email."}

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    print(f"DEBUG: Login Attempt - Username: {form_data.username}")
    q = await db.execute(select(User).where(User.email == form_data.username))
    user = q.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if getattr(user, "is_email_verified", False) == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified. Please verify your email first.")
        
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/verify-email")
async def verify_email(req: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.email == req.email))
    user = q.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_email_verified:
        return {"message": "Email already verified"}
    if user.otp_code != req.otp_code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
        
    user.is_email_verified = True
    user.otp_code = None
    await db.commit()
    return {"message": "Email verified successfully"}