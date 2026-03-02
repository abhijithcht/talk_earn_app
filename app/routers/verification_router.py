from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User, BannedID, AuditLog
from app.schemas import VerificationSubmit
from app.dependencies import get_current_active_user
from sqlalchemy import select

router = APIRouter(prefix="/verification", tags=["verification"])

@router.post("/submit")
async def submit_verification(
    data: VerificationSubmit, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if ID hash is banned
    q = await db.execute(select(BannedID).where(BannedID.id_hash == data.id_hash))
    banned = q.scalars().first()
    if banned:
        raise HTTPException(status_code=403, detail="This ID is blacklisted.")
    
    current_user.id_hash = data.id_hash
    current_user.date_of_birth = data.date_of_birth
    current_user.verification_status = "pending" # Needs admin approval
    
    # Log the action (Audit)
    audit = AuditLog(target_user_id=current_user.id, action="verification_submitted", details="User uploaded ID and selfie")
    db.add(audit)
    
    await db.commit()
    return {"message": "Verification submitted successfully. Pending admin review."}

@router.get("/status")
async def get_status(current_user: User = Depends(get_current_active_user)):
    return {
        "status": current_user.verification_status,
        "is_verified": current_user.is_verified
    }
