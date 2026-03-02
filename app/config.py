from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database - defaults to SQLite for local dev. 
    # Set DATABASE_URL=mysql+aiomysql://user:pass@host:3306/dbname in .env for MySQL
    DATABASE_URL: str = "sqlite+aiosqlite:///./talk_earn.db"
    
    # JWT
    SECRET_KEY: str = "change_me_in_production_please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720  # 12 hours
    
    # Coin rates per minute of call
    TEXT_COINS_PER_MIN: int = 1
    AUDIO_COINS_PER_MIN: int = 2
    VIDEO_COINS_PER_MIN: int = 5
    
    # Email SMTP (for OTP verification)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None
    
    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
