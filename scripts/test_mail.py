import asyncio
import aiosmtplib
from email.message import EmailMessage

async def test_mailpit():
    print("Testing Mailpit connection on 127.0.0.1:1025...")
    message = EmailMessage()
    message["From"] = "test@talkearn.com"
    message["To"] = "verify@test.com"
    message["Subject"] = "Mailpit Test"
    message.set_content("This is a test message to verify Mailpit configuration.")

    try:
        await aiosmtplib.send(
            message,
            hostname="127.0.0.1",
            port=1025,
            use_tls=False,
            start_tls=False
        )
        print("SUCCESS: Message sent to Mailpit!")
    except Exception as e:
        print(f"FAILED: Could not send to Mailpit: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_mailpit())
