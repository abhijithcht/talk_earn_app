# 📡 API Reference

Base URL: `http://127.0.0.1:8000`

> Interactive docs available at [`/docs`](http://127.0.0.1:8000/docs) (Swagger UI) and [`/redoc`](http://127.0.0.1:8000/redoc)

---

## Auth (`/auth`)

| Method | Endpoint             | Auth | Description                                               |
| ------ | -------------------- | ---- | --------------------------------------------------------- |
| POST   | `/auth/register`     | ❌    | Register a new user. Sends OTP email.                     |
| POST   | `/auth/token`        | ❌    | Login. Returns JWT access token. Requires verified email. |
| POST   | `/auth/verify-email` | ❌    | Verify email with OTP code.                               |

### Register
```json
POST /auth/register
Body: { "email": "user@example.com", "password": "secret", "gender": "male" }
Response: { "message": "registered. Please verify your email." }
```

### Login
```json
POST /auth/token
Body: { "email": "user@example.com", "password": "secret" }
Response: { "access_token": "eyJ...", "token_type": "bearer" }
```

---

## Wallet (`/wallet`)

| Method | Endpoint           | Auth | Description                               |
| ------ | ------------------ | ---- | ----------------------------------------- |
| POST   | `/wallet/earn`     | 🔒    | Earn coins for call time.                 |
| GET    | `/wallet/balance`  | 🔒    | Get current coin balance.                 |
| POST   | `/wallet/withdraw` | 🔒    | Withdraw coins via Stripe. Min 100 coins. |

### Earn Coins
```json
POST /wallet/earn
Body: { "minutes": 10, "medium": "audio" }
Response: { "message": "coins added", "balance": 30 }
```

Coin rates: text=1/min, audio=2/min, video=5/min. Rating bonuses applied automatically.

---

## Chat (`/chat`) — WebSocket

| Protocol | Endpoint                      | Description                                          |
| -------- | ----------------------------- | ---------------------------------------------------- |
| WS       | `/chat/ws/global/{user_name}` | Global lobby — broadcast to all connected users      |
| WS       | `/chat/ws/{user_id}`          | Private 1-on-1 signaling (WebRTC offers/answers/ICE) |

---

## Profile (`/profile`)

| Method | Endpoint                   | Auth | Description                                      |
| ------ | -------------------------- | ---- | ------------------------------------------------ |
| GET    | `/profile/me`              | 🔒    | Get current user profile.                        |
| PUT    | `/profile/update`          | 🔒    | Update profile (name, gender, preferences, etc.) |
| GET    | `/profile/avatars`         | 🔒    | List available avatars.                          |
| POST   | `/profile/picture`         | 🔒    | Upload profile picture (multipart).              |
| POST   | `/profile/change-password` | 🔒    | Change password.                                 |
| DELETE | `/profile/delete-account`  | 🔒    | Delete account.                                  |

---

## Match (`/match`)

| Method | Endpoint        | Auth | Description           |
| ------ | --------------- | ---- | --------------------- |
| POST   | `/match/find`   | 🔒    | Enter matching queue. |
| POST   | `/match/cancel` | 🔒    | Cancel matching.      |

---

## Verification (`/verification`)

| Method | Endpoint               | Auth | Description                                       |
| ------ | ---------------------- | ---- | ------------------------------------------------- |
| POST   | `/verification/submit` | 🔒    | Submit ID verification (id_hash + date of birth). |
| GET    | `/verification/status` | 🔒    | Check verification status.                        |

---

## Moderation (`/moderation`)

| Method | Endpoint                          | Auth | Description                    |
| ------ | --------------------------------- | ---- | ------------------------------ |
| POST   | `/moderation/warn/{user_id}`      | 🔒    | Issue warning to user (admin). |
| POST   | `/moderation/appeal/{warning_id}` | 🔒    | Appeal a warning.              |

---

## Admin (`/admin`)

| Method | Endpoint                                 | Auth | Description                 |
| ------ | ---------------------------------------- | ---- | --------------------------- |
| GET    | `/admin/verifications/pending`           | 🔒👑   | List pending verifications. |
| POST   | `/admin/verifications/{user_id}/approve` | 🔒👑   | Approve user verification.  |
| POST   | `/admin/verifications/{user_id}/reject`  | 🔒👑   | Reject user verification.   |
| POST   | `/admin/ban/{user_id}`                   | 🔒👑   | Ban a user.                 |

Legend: ❌ = No auth, 🔒 = Bearer token, 👑 = Admin only
