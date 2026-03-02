from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    gender: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class WalletOut(BaseModel):
    balance: int


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class AccountDelete(BaseModel):
    current_password: str