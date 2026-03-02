from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User, Warning, AuditLog
from app.dependencies import get_current_active_user
from pydantic import BaseModel

router = APIRouter(prefix="/moderation", tags=["moderation"])

class WarnRequest(BaseModel):
    reason: str

@router.post("/warn/{user_id}")
async def warn_user(
    user_id: int, 
    req: WarnRequest,
    admin: User = Depends(get_current_active_user), # Expect admin role in real app
    db: AsyncSession = Depends(get_db)
):
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.warnings += 1
    
    # Determine level
    level = "reminder"
    if user.warnings == 2:
        level = "freeze"
    elif user.warnings >= 3:
        level = "ban"
        user.is_active = False
        
    w = Warning(user_id=user.id, level=level, reason=req.reason)
    db.add(w)
    
    # Audit log
    audit = AuditLog(admin_id=admin.id, target_user_id=user.id, action=f"issued_warning_{level}", details=req.reason)
    db.add(audit)
    
    await db.commit()
    return {"warnings": user.warnings, "level": level, "active": user.is_active}

@router.post("/appeal/{warning_id}")
async def appeal_warning(
    warning_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    q = await db.execute(select(Warning).where(Warning.id == warning_id, Warning.user_id == current_user.id))
    w = q.scalars().first()
    if not w:
        raise HTTPException(status_code=404, detail="Warning not found")
        
    if w.appealed:
        raise HTTPException(status_code=400, detail="Already appealed")
        
    w.appealed = True
    await db.commit()
    return {"message": "Appeal submitted successfully. A moderator will review it."}