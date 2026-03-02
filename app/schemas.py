from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    gender: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    otp_code: str

class TokenData(BaseModel):
    id: Optional[str] = None

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    gender: Optional[str] = None
    gender_preference: Optional[str] = None
    avatar_id: Optional[int] = None
    customizations: Optional[str] = None
    interests: Optional[str] = None

class MatchRequest(BaseModel):
    medium: str  # 'text', 'audio', 'video'

class EarnRequest(BaseModel):
    minutes: int
    medium: str

class VerificationSubmit(BaseModel):
    id_hash: str
    date_of_birth: datetime

class WalletOut(BaseModel):
    balance: int

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class AccountDelete(BaseModel):
    current_password: str
