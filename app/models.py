from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Avatar(Base):
    __tablename__ = "avatars"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(512), nullable=False)
    category = Column(String(64), nullable=True)  # neutral, gender-specific, cultural, fun

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(512), nullable=False)
    
    # Base flags
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Email OTP 
    is_email_verified = Column(Boolean, default=False)
    otp_code = Column(String(16), nullable=True)
    
    # Verification & Compliance
    verification_status = Column(String(32), default="pending") # pending, verified, rejected
    id_hash = Column(String(255), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    
    # Profile & Preferences
    gender = Column(String(16), nullable=True)
    gender_preference = Column(String(16), default="any") # male, female, any
    profile_picture_url = Column(String(512), nullable=True)
    avatar_id = Column(Integer, ForeignKey("avatars.id"), nullable=True)
    customizations = Column(Text, nullable=True) # JSON literal for colors/accessories
    interests = Column(Text, nullable=True)
    
    # Ratings & Moderation
    rating = Column(Float, default=5.0)
    warnings = Column(Integer, default=0)
    withdrawal_blocked = Column(Boolean, default=False)
    stripe_account_id = Column(String(255), nullable=True) # Linked payout account
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    wallet = relationship("Wallet", back_populates="user", uselist=False)

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    balance = Column(Integer, default=0)  # coins
    user = relationship("User", back_populates="wallet")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    coins = Column(Integer)
    type = Column(String(32))  # "earn", "withdraw", "bonus"
    status = Column(String(32), default="completed") # pending, completed, failed
    payout_provider = Column(String(64), nullable=True) # e.g. Stripe, PayPal
    created_at = Column(DateTime, default=datetime.utcnow)

class SessionRecord(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    caller_id = Column(Integer, ForeignKey("users.id"))
    callee_id = Column(Integer, ForeignKey("users.id"))
    session_type = Column(String(16), default="text") # text, audio, video
    duration_minutes = Column(Integer)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    target_user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(128), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class BannedID(Base):
    __tablename__ = "banned_ids"
    id = Column(Integer, primary_key=True, index=True)
    id_hash = Column(String(255), unique=True, index=True, nullable=False)
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Follow(Base):
    __tablename__ = "follows"
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    followed_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class Warning(Base):
    __tablename__ = "warnings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    level = Column(String(32), nullable=False) # reminder, freeze, ban
    reason = Column(String(255), nullable=True)
    appealed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
