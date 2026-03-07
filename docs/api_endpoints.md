# API Endpoints Documentation

The Talk & Earn Python backend has a total of **25** endpoints defined across 9 routers.

## 1. Auth (`/auth`)
- `POST /auth/register`
- `POST /auth/token`
- `POST /auth/verify-email`

## 2. Admin (`/admin`)
- `GET /admin/verifications/pending`
- `POST /admin/verifications/{user_id}/approve`
- `POST /admin/verifications/{user_id}/reject`
- `POST /admin/ban/{user_id}`

## 3. Chat (`/chat`)
- `WS /chat/ws/global/{user_name}`
- `WS /chat/ws/{user_id}`

## 4. Match (`/match`)
- `POST /match/random`
- `POST /match/cancel`

## 5. Moderation (`/moderation`)
- `POST /moderation/warn/{user_id}`
- `POST /moderation/appeal/{warning_id}`

## 6. Profile (`/profile`)
- `GET /profile/avatars`
- `PUT /profile/`
- `PUT /profile/password`
- `POST /profile/account/delete`
- `GET /profile/me`
- `POST /profile/picture/upload`

## 7. Rating (`/rating`)
- `POST /rating/submit`

## 8. Verification (`/verification`)
- `POST /verification/submit`
- `GET /verification/status`

## 9. Wallet (`/wallet`)
- `POST /wallet/earn`
- `GET /wallet/balance`
- `POST /wallet/withdraw`
