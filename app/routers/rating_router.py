from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.database import get_db
from app.models import User, SessionRecord
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/rating", tags=["rating"])

class RatingSubmit(BaseModel):
    target_user_id: int
    score: int # 1 to 5

@router.post("/submit")
async def submit_rating(
    data: RatingSubmit,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if data.score < 1 or data.score > 5:
        raise HTTPException(status_code=400, detail="Score must be between 1 and 5.")
        
    q = await db.execute(select(User).where(User.id == data.target_user_id))
    target = q.scalars().first()
    
    if not target:
        raise HTTPException(status_code=404, detail="Target user not found.")
        
    # In a full-scale app, we would sum the SessionRecords.
    # For now, we mathematically roll the average slightly towards the new score
    target.rating = round((target.rating * 0.9) + (data.score * 0.1), 2)
    
    # Store the discrete rating
    session = SessionRecord(
        caller_id=current_user.id,
        callee_id=data.target_user_id,
        rating=data.score,
        duration_minutes=1
    )
    db.add(session)
    await db.commit()
    
    return {"message": "Rating submitted successfully.", "new_average": target.rating}
