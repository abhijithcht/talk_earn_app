import stripe
from fastapi import HTTPException
from app.config import settings

# In a real production app, this would be set in an .env file
# e.g., stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_key = "sk_test_dummy_key_12345"

async def process_payout(stripe_account_id: str, amount_cents: int, currency: str = "usd"):
    """
    Initiates a formal Stripe Transfer to a connected Express account.
    """
    if not stripe_account_id:
        raise HTTPException(
            status_code=400, 
            detail="User does not have a linked Stripe Account. Please connect one first."
        )
        
    try:
        # Create a Transfer to the connected account
        transfer = stripe.Transfer.create(
            amount=amount_cents,
            currency=currency,
            destination=stripe_account_id,
            description="Talk & Earn Platform Payout"
        )
        return transfer
    except stripe.error.StripeError as e:
        # Catch Stripe specific errors (e.g., insufficient platform balance, invalid account)
        raise HTTPException(status_code=400, detail=f"Stripe Error: {str(e)}")
    except Exception as e:
        # Catch generic exceptions
        raise HTTPException(status_code=500, detail="Internal payout processing error.")
