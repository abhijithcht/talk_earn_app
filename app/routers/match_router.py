from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from typing import Dict, List
from app.database import get_db
from app.models import User
from app.dependencies import get_current_active_user
from app.schemas import MatchRequest

router = APIRouter(prefix="/match", tags=["match"])

# Simple in-memory waiting pool
# waiting_pool mapped by medium -> user's own gender
waiting_pool: Dict[str, Dict[str, List[int]]] = {
    "text": {"male": [], "female": [], "other": []},
    "audio": {"male": [], "female": [], "other": []},
    "video": {"male": [], "female": [], "other": []}
}
pool_lock = asyncio.Lock()

@router.post("/random")
async def find_random_match(
    req: MatchRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    pref = current_user.gender_preference or "any"
    user_gender = current_user.gender or "other"
    medium = req.medium
    
    if medium not in waiting_pool:
        raise HTTPException(status_code=400, detail="Invalid communication medium selected.")
    
    async with pool_lock:
        if pref == "any":
            # Pop someone available from any gender pool within the SAME medium
            for gender_key in waiting_pool[medium].keys():
                if waiting_pool[medium][gender_key]:
                    matched_id = waiting_pool[medium][gender_key].pop(0)
                    if matched_id != current_user.id:
                        # Fetch the matched user's metadata for the UI
                        target_user = await db.get(User, matched_id)
                        return {
                            "matched_user_id": matched_id,
                            "matched_user_name": target_user.full_name or f"User {matched_id}",
                            "matched_user_customizations": target_user.customizations
                        }
        else:
            # Pop specifically from preference pool
            if pref in waiting_pool[medium] and waiting_pool[medium][pref]:
                matched_id = waiting_pool[medium][pref].pop(0)
                if matched_id != current_user.id:
                    target_user = await db.get(User, matched_id)
                    return {
                        "matched_user_id": matched_id,
                        "matched_user_name": target_user.full_name or f"User {matched_id}",
                        "matched_user_customizations": target_user.customizations
                    }
        
        # No match found; add self to waiting pool
        if current_user.id not in waiting_pool[medium][user_gender]:
            waiting_pool[medium][user_gender].append(current_user.id)
            
    return {"message": f"Added to {medium} waiting pool. Waiting for another user..."}

@router.post("/cancel")
async def cancel_match(
    req: MatchRequest,
    current_user: User = Depends(get_current_active_user)
):
    medium = req.medium
    user_gender = current_user.gender or "other"
    
    if medium not in waiting_pool:
        return {"message": "Invalid medium."}
        
    async with pool_lock:
        if current_user.id in waiting_pool[medium][user_gender]:
            waiting_pool[medium][user_gender].remove(current_user.id)
            return {"message": "Successfully removed from waiting pool."}
            
    return {"message": "User was not in the waiting pool."}
