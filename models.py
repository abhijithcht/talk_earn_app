from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    gender = Column(String, nullable=True)
    rating = Column(Float, default=5.0)
    warnings = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

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
    type = Column(String)  # "earn", "withdraw", "bonus"
    created_at = Column(DateTime, default=datetime.utcnow)

class SessionRecord(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    caller_id = Column(Integer, ForeignKey("users.id"))
    callee_id = Column(Integer, ForeignKey("users.id"))
    duration_minutes = Column(Integer)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)