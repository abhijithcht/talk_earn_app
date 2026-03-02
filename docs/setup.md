# 🛠️ Setup Guide

Step-by-step instructions to get Talk & Earn running locally on **Windows 11**.

---

## Prerequisites

| Tool               | Version | Download                                                                                      |
| ------------------ | ------- | --------------------------------------------------------------------------------------------- |
| **Python**         | 3.12+   | [python.org](https://www.python.org/downloads/)                                               |
| **Node.js**        | 18+     | [nodejs.org](https://nodejs.org/)                                                             |
| **Git**            | Latest  | [git-scm.com](https://git-scm.com/)                                                           |
| **Android Studio** | Latest  | [developer.android.com](https://developer.android.com/studio) *(optional, for mobile builds)* |

---

## 1. Clone the Repository

```powershell
git clone <repo-url>
cd talk_earn_app
```

---

## 2. Python Virtual Environment

```powershell
# Create the virtual environment
python -m venv .venv

# Activate it (PowerShell)
.\.venv\Scripts\Activate.ps1

# Install all Python dependencies
pip install -r requirements.txt
```

> ⚠️ Always activate the venv before running the server or tests. Your prompt should show `(.venv)`.

---

## 3. Environment Variables

```powershell
# Copy the template
Copy-Item .env.example .env
```

Open `.env` and fill in the real values:

| Variable                      | Required | Description                                                          |
| ----------------------------- | -------- | -------------------------------------------------------------------- |
| `DATABASE_URL`                | ✅        | Default SQLite works out of the box. Change to MySQL for production. |
| `SECRET_KEY`                  | ✅        | A long random string for JWT signing. **Change this!**               |
| `ALGORITHM`                   | ✅        | JWT algorithm. Keep `HS256`.                                         |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ✅        | Token lifetime. Default: `720` (12 hours).                           |
| `SMTP_HOST`                   | ❌        | Gmail SMTP host for OTP emails (e.g. `smtp.gmail.com`).              |
| `SMTP_PORT`                   | ❌        | SMTP port. Default: `587`.                                           |
| `SMTP_USER`                   | ❌        | Your email for sending OTP codes.                                    |
| `SMTP_PASS`                   | ❌        | App-specific password for SMTP.                                      |
| `STRIPE_SECRET_KEY`           | ❌        | Stripe test key for payout integration.                              |
| `TEXT_COINS_PER_MIN`          | ✅        | Coins earned per minute of text chat. Default: `1`.                  |
| `AUDIO_COINS_PER_MIN`         | ✅        | Coins earned per minute of audio call. Default: `2`.                 |
| `VIDEO_COINS_PER_MIN`         | ✅        | Coins earned per minute of video call. Default: `5`.                 |

---

## 4. Run the Backend Server

```powershell
uvicorn app.main:app --reload --port 8000
```

The server starts at `http://127.0.0.1:8000`. The database tables are auto-created on first startup.

### API Docs (auto-generated)

| URL                           | Description              |
| ----------------------------- | ------------------------ |
| `http://127.0.0.1:8000/docs`  | Swagger UI (interactive) |
| `http://127.0.0.1:8000/redoc` | ReDoc (read-only)        |

---

## 5. Run Tests

```powershell
.\.venv\Scripts\Activate.ps1
pytest test_api.py -v
```

Tests cover:
- Full auth flow (register → login → token)
- Wallet operations (earn → withdraw with mocked Stripe)
- Admin verification flow (submit → approve → verified)

---

## 6. Mobile Build (Optional)

The Flutter app under `flutter_app/` is a WebView wrapper that loads the web frontend.

```powershell
cd flutter_app
flutter pub get
flutter run
```

For a standalone APK build, see [`apk_build_guide.md`](../apk_build_guide.md).

---

## 7. Node / Capacitor (Optional)

Only needed if you want to build the Capacitor Android shell:

```powershell
npm install
npx cap sync
npx cap open android
```

---

## Project Structure

```
talk_earn_app/
├── app/                    # Python FastAPI backend
│   ├── main.py             # Entry point
│   ├── config.py           # Settings from .env
│   ├── database.py         # Async SQLAlchemy
│   ├── models.py           # ORM models
│   ├── schemas.py          # Pydantic schemas
│   ├── auth.py             # JWT helpers
│   ├── routers/            # API endpoints
│   └── services/           # Business logic
├── flutter_app/            # Flutter WebView mobile app
├── www/                    # Web frontend (JS + HTML)
├── static/uploads/         # User-uploaded files
├── docs/                   # Documentation
│   ├── Environment.md      # Target architecture roadmap
│   ├── Features.md         # Target feature & tech stack
│   └── setup.md            # ← You are here
├── .env.example            # Environment template
├── requirements.txt        # Python deps
├── package.json            # Node deps
└── test_api.py             # Integration tests
```

---

## Troubleshooting

| Problem               | Solution                                                                       |
| --------------------- | ------------------------------------------------------------------------------ |
| `ModuleNotFoundError` | Make sure the venv is activated: `.\.venv\Scripts\Activate.ps1`                |
| `Database locked`     | Close any other process using `talk_earn.db`                                   |
| API returns 401       | Token expired. Re-login at `/auth/token`.                                      |
| SMTP errors           | Set `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS` in `.env`. Use a Gmail App Password. |
