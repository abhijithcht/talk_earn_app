import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import engine, Base

@pytest.mark.asyncio
async def test_full_auth_and_profile_flow():
    # 0. Setup Database Tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

    # Use ASGITransport for testing async FastAPI apps
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        # 1. Register
        response = await client.post(
            "/auth/register",
            json={"email": test_email, "password": "securepassword", "gender": "male"}
        )
        assert response.status_code == 200, f"Register failed: {response.text}"

        # 2. Verify Email (fetch OTP from DB)
        from sqlalchemy import select as sa_select
        from app.models import User as UserModel
        from app.database import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            q = await session.execute(sa_select(UserModel).where(UserModel.email == test_email))
            registered_user = q.scalars().first()
            otp_code = registered_user.otp_code

        response = await client.post(
            "/auth/verify-email",
            json={"email": test_email, "otp_code": otp_code}
        )
        assert response.status_code == 200, f"Verify email failed: {response.text}"

        # 3. Login
        response = await client.post(
            "/auth/token",
            json={"email": test_email, "password": "securepassword"}
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        token = response.json().get("access_token")

        headers = {"Authorization": f"Bearer {token}"}

        # 3. Access Profile Avatars
        response = await client.get("/profile/avatars", headers=headers)
        assert response.status_code == 200, f"Avatars failed: {response.text}"
        assert isinstance(response.json(), list)

        # 4. Check Wallet Balance
        response = await client.get("/wallet/balance", headers=headers)
        assert response.status_code == 200, f"Balance failed: {response.text}"
        assert response.json() == {"balance": 0}

        # 5. Earn Coins (audio: 10 min * 2 coins/min = 20, + 50% bonus for 5.0 rating = 30)
        response = await client.post(
            "/wallet/earn",
            json={"minutes": 10, "medium": "audio"},
            headers=headers
        )
        assert response.status_code == 200, f"Earn failed: {response.text}"
        assert response.json()["balance"] == 30

        # 6. Earn more to reach withdrawal minimum
        response = await client.post(
            "/wallet/earn",
            json={"minutes": 50, "medium": "audio"},
            headers=headers
        )
        assert response.status_code == 200, f"Earn more failed: {response.text}"
        # 50 * 2 = 100 + 50% = 150, total = 30 + 150 = 180
        assert response.json()["balance"] == 180

        # 7. Withdraw Request - Should FAIL (No Stripe ID linked)
        response = await client.post(
            "/wallet/withdraw",
            json={"payout_provider": "stripe", "amount": 100},
            headers=headers
        )
        assert response.status_code == 400
        assert "Stripe Account" in response.text

        # 8. Manually link Stripe Account in DB
        from sqlalchemy import select
        from app.models import User
        from app.database import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            q = await session.execute(select(User).where(User.email == test_email))
            test_user = q.scalars().first()
            test_user.stripe_account_id = "acct_testdummy123"
            await session.commit()

        # 9. Withdraw Request - SUCCESS (Mocked Stripe Transfer)
        from unittest.mock import patch, MagicMock
        mock_transfer = MagicMock()
        mock_transfer.id = "tr_mock_transaction_123"

        with patch('app.services.payment_service.stripe.Transfer.create', return_value=mock_transfer):
            response = await client.post(
                "/wallet/withdraw",
                json={"payout_provider": "stripe", "amount": 100},
                headers=headers
            )
            assert response.status_code == 200, f"Withdraw failed: {response.text}"
            assert response.json()["remaining_balance"] == 80  # 180 - 100
            assert response.json()["transfer_id"] == "tr_mock_transaction_123"

    # 9. Teardown
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_admin_verification_flow():
    # Setup Data
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    admin_email = f"admin_{uuid.uuid4().hex[:8]}@example.com"
    user_email = f"user_{uuid.uuid4().hex[:8]}@example.com"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register Admin & User
        await client.post("/auth/register", json={"email": admin_email, "password": "pass", "gender": "male"})
        await client.post("/auth/register", json={"email": user_email, "password": "pass", "gender": "female"})

        # Verify emails & promote Admin in DB
        from sqlalchemy import select
        from app.models import User
        from app.database import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            q = await session.execute(select(User).where(User.email == admin_email))
            admin_user = q.scalars().first()
            admin_otp = admin_user.otp_code
            admin_user.is_superuser = True

            q2 = await session.execute(select(User).where(User.email == user_email))
            normal_user = q2.scalars().first()
            user_otp = normal_user.otp_code
            await session.commit()

        # Verify both emails
        await client.post("/auth/verify-email", json={"email": admin_email, "otp_code": admin_otp})
        await client.post("/auth/verify-email", json={"email": user_email, "otp_code": user_otp})

        # Login
        admin_res = await client.post("/auth/token", json={"email": admin_email, "password": "pass"})
        admin_token = admin_res.json().get("access_token")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        user_res = await client.post("/auth/token", json={"email": user_email, "password": "pass"})
        user_token = user_res.json().get("access_token")
        user_headers = {"Authorization": f"Bearer {user_token}"}

        # User submits verification
        response = await client.post(
            "/verification/submit",
            json={"id_hash": "hash_123", "date_of_birth": "1995-01-01T00:00:00Z"},
            headers=user_headers
        )
        assert response.status_code == 200

        # Admin views pending
        response = await client.get("/admin/verifications/pending", headers=admin_headers)
        assert response.status_code == 200
        pending_list = response.json()
        target_user = next((u for u in pending_list if u["email"] == user_email), None)
        assert target_user is not None
        target_id = target_user["id"]

        # Admin approves
        response = await client.post(f"/admin/verifications/{target_id}/approve", headers=admin_headers)
        assert response.status_code == 200

        # Verify status
        response = await client.get("/verification/status", headers=user_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "verified"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
