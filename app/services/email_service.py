import random

async def send_otp_email(to_email: str, otp_code: str):
    """
    Mock Email Service. 
    In production, this would use aiosmtplib to connect to SendGrid or Gmail.
    For local testing, we just print the OTP to the fastAPI console.
    """
    subject = "Verify Your Talk & Earn Account"
    body = f"Your verification code is: {otp_code}\nPlease enter this code to activate your account."
    
    print("\n" + "="*50)
    print(f"📧 MOCK EMAIL SENT TO: {to_email}")
    print(f"Subject: {subject}")
    print(f"Code: {otp_code}")
    print("="*50 + "\n")
    
    # Simulate network delay for realism
    import asyncio
    await asyncio.sleep(1)
    
    return True
