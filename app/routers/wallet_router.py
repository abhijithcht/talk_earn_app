from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.database import get_db
from app.models import Wallet, Transaction, User
from app.config import settings
from app.dependencies import get_current_active_user
from app.services.payment_service import process_payout
from app.schemas import EarnRequest

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.post("/earn")
async def earn_coins(req: EarnRequest, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    # Base calculation based on selected communication medium
    if req.medium == 'video':
        base_rate = settings.VIDEO_COINS_PER_MIN
    elif req.medium == 'audio':
        base_rate = settings.AUDIO_COINS_PER_MIN
    else:
        base_rate = settings.TEXT_COINS_PER_MIN
        
    coins = req.minutes * base_rate
    
    # Tiered Bonus logic for high and low ratings
    if current_user.rating >= 4.8:
        coins += int(coins * 0.50) # 50% massive bonus
    elif current_user.rating >= 4.0:
        coins += int(coins * 0.20) # 20% good bonus
    elif current_user.rating < 3.0:
        coins -= int(coins * 0.20) # 20% penalty for poor behavior
        
    q = await db.execute(select(Wallet).where(Wallet.user_id == current_user.id))
    wallet = q.scalars().first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
        
    wallet.balance += coins

    tx = Transaction(user_id=current_user.id, coins=coins, type="earn", status="completed")
    db.add(tx)
    await db.commit()
    return {"message": "coins added", "balance": wallet.balance}

@router.get("/balance")
async def get_balance(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Wallet).where(Wallet.user_id == current_user.id))
    wallet = q.scalars().first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"balance": wallet.balance}

class WithdrawalRequest(BaseModel):
    payout_provider: str
    amount: int

@router.post("/withdraw")
async def withdraw_coins(
    req: WithdrawalRequest, 
    current_user: User = Depends(get_current_active_user), 
    db: AsyncSession = Depends(get_db)
):
    # Quality Control Limits
    if current_user.rating < 3.0 or current_user.withdrawal_blocked:
        raise HTTPException(status_code=403, detail="Withdrawals are blocked (low rating or moderated).")
        
    # Validation Limit
    if req.amount < 100:
        raise HTTPException(status_code=400, detail="Minimum withdrawal is 100 coins ($1).")
        
    q = await db.execute(select(Wallet).where(Wallet.user_id == current_user.id))
    wallet = q.scalars().first()
    
    if wallet.balance < req.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance.")
        
    # Calculate cents for Stripe (e.g. 100 coins = $1.00 = 100 cents)
    # The payout ratio is 1 coin = 1 cent
    amount_in_cents = req.amount
    
    # Process Payout Synchronously
    transfer = await process_payout(
        stripe_account_id=current_user.stripe_account_id, 
        amount_cents=amount_in_cents
    )
        
    # Only deduct if the transfer was successful
    wallet.balance -= req.amount
    
    tx = Transaction(
        user_id=current_user.id, 
        coins=-req.amount, 
        type="withdraw", 
        status="completed", # Reaching here guarantees success
        payout_provider=f"Stripe Transfer: {transfer.id}"
    )
    db.add(tx)
    await db.commit()
    
    return {
        "message": "Withdrawal processed securely to Stripe account.", 
        "remaining_balance": wallet.balance,
        "transfer_id": transfer.id
    }