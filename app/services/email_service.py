import aiosmtplib
from email.message import EmailMessage
from app.config import settings

async def send_otp_email(to_email: str, otp_code: str):
    """
    Sends an OTP email via SMTP using aiosmtplib.
    Configured via environment variables (SMTP_HOST, SMTP_PORT, etc.).
    """
    if not settings.SMTP_HOST:
        print("\n" + "!"*50)
        print(f"[MISSING SMTP CONFIG] TO: {to_email} | Code: {otp_code}")
        print("!"*50 + "\n")
        return False

    message = EmailMessage()
    message["From"] = settings.SMTP_USER or "noreply@talkearn.com"
    message["To"] = to_email
    message["Subject"] = "Verify Your Talk & Earn Account"
    message.set_content(f"Your verification code is: {otp_code}\nPlease enter this code to activate your account.")

    try:
        smtp_args = {
            "hostname": settings.SMTP_HOST,
            "port": settings.SMTP_PORT,
            "use_tls": settings.SMTP_PORT == 465,
            "start_tls": settings.SMTP_PORT == 587,
        }
        if settings.SMTP_USER:
            smtp_args["username"] = settings.SMTP_USER
        if settings.SMTP_PASS:
            smtp_args["password"] = settings.SMTP_PASS

        await aiosmtplib.send(message, **smtp_args)
        print(f"DEBUG: Email sent successfully to {to_email} via {settings.SMTP_HOST}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to send email to {to_email}: {str(e)}")
        # Fallback to console print so developers don't get blocked
        print("\n" + "="*50)
        print(f"[SMTP FALLBACK PRINT] TO: {to_email} | Code: {otp_code}")
        print("="*50 + "\n")
        return False
