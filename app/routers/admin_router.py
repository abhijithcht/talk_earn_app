from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User, AuditLog
from app.dependencies import get_current_admin_user
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/verifications/pending")
async def get_pending_verifications(
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    q = await db.execute(select(User).where(User.verification_status == "pending"))
    users = q.scalars().all()
    
    return [
        {
            "id": u.id,
            "email": u.email,
            "date_of_birth": u.date_of_birth,
            "submitted_at": u.created_at # In real app, might use a separate VerificationRequest table
        }
        for u in users
    ]

@router.post("/verifications/{user_id}/approve")
async def approve_verification(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.verification_status != "pending":
        raise HTTPException(status_code=400, detail=f"Status is {user.verification_status}")
        
    user.verification_status = "verified"
    user.is_verified = True
    
    audit = AuditLog(admin_id=admin.id, target_user_id=user.id, action="verification_approved")
    db.add(audit)
    
    await db.commit()
    return {"message": "Verification approved"}

class RejectionRequest(BaseModel):
    reason: str

@router.post("/verifications/{user_id}/reject")
async def reject_verification(
    user_id: int,
    req: RejectionRequest,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.verification_status = "rejected"
    user.is_verified = False # ensure explicitly false
    
    audit = AuditLog(admin_id=admin.id, target_user_id=user.id, action="verification_rejected", details=req.reason)
    db.add(audit)
    
    await db.commit()
    return {"message": f"Verification rejected: {req.reason}"}

class AdminBanRequest(BaseModel):
    reason: str

@router.post("/ban/{user_id}")
async def admin_ban_user(
    user_id: int,
    req: AdminBanRequest,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.is_active = False # Severing JWT access instantly
    
    audit = AuditLog(admin_id=admin.id, target_user_id=user.id, action="manual_ban", details=req.reason)
    db.add(audit)
    
    await db.commit()
    return {"message": "User permanently banned"}
