# 🎙️ Talk & Earn

**Earn real money by talking to people around the world.**

Talk & Earn is a social platform that connects users through random audio, video, and text conversations — and rewards them with coins for every minute spent chatting. Once you've earned enough, cash out directly to your bank.

---

## 💡 How It Works

1. **Sign Up** — Create an account and verify your identity
2. **Get Matched** — Tap "Find Match" and get paired with a random user based on your gender preference
3. **Talk & Earn Coins** — Earn coins for every minute of conversation:
   | Mode  | Rate        |
   | ----- | ----------- |
   | Text  | 1 coin/min  |
   | Audio | 2 coins/min |
   | Video | 5 coins/min |
4. **Cash Out** — Withdraw when you reach 100 coins ($1 USD) via Stripe

---

## ✨ Features

| Feature               | Description                                                   |
| --------------------- | ------------------------------------------------------------- |
| 🎲 **Random Matching** | Gender-preference matching queue with real-time pairing       |
| 💰 **Coin Wallet**     | Earn, track, and withdraw coins with full transaction history |
| 🎭 **Avatar System**   | Choose from a library of default avatars or upload your own   |
| 🔐 **Verification**    | ID + selfie verification flow with admin approval             |
| ⚖️ **Moderation**      | 3-level warning system (reminder → freeze → ban)              |
| ⭐ **Rating System**   | Post-call ratings with bonus coins for high-rated users       |
| 👤 **Profiles**        | Customizable profiles with bio, avatar, and settings          |
| 🛡️ **Admin Panel**     | User management, verification approval, and moderation tools  |

---

## 🏗️ Architecture

```
talk_earn_app/
├── app/                    # FastAPI backend (Python)
│   ├── main.py             # App entry point + CORS + router mounting
│   ├── config.py           # Pydantic settings (env-driven)
│   ├── database.py         # Async SQLAlchemy engine + session
│   ├── models.py           # User, Wallet, Transaction, Session models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── auth.py             # JWT token creation
│   ├── routers/            # 8 API router modules
│   │   ├── auth_router.py
│   │   ├── wallet_router.py
│   │   ├── chat_router.py
│   │   ├── match_router.py
│   │   ├── profile_router.py
│   │   ├── verification_router.py
│   │   ├── moderation_router.py
│   │   └── admin_router.py
│   └── services/           # Business logic (email, payments)
├── flutter_app/            # Flutter mobile wrapper (WebView)
├── android/                # Capacitor Android shell
├── www/                    # Web frontend (JS + HTML)
│   ├── index.html
│   └── app.js
├── docs/                   # Architecture & feature docs
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── package.json            # Node/Capacitor dependencies
```

### Tech Stack (Current Prototype)

| Layer            | Technology                                    |
| ---------------- | --------------------------------------------- |
| **Backend**      | Python 3.13 · FastAPI · Async SQLAlchemy      |
| **Database**     | SQLite (dev) · MySQL (prod-ready)             |
| **Auth**         | JWT via python-jose · bcrypt passwords        |
| **Payments**     | Stripe Connect                                |
| **Web Frontend** | Vanilla JS · HTML/CSS                         |
| **Mobile**       | Capacitor (Android) + Flutter WebView wrapper |

> 📌 See [`docs/Environment.md`](docs/Environment.md) and [`docs/Features.md`](docs/Features.md) for the **target architecture** roadmap (Flutter native + NestJS + PostgreSQL + Redis).

---

## 🚀 Quick Start

```powershell
# Clone & enter
git clone <repo-url>
cd talk_earn_app

# Python venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Environment
Copy-Item .env.example .env
# Edit .env with your real values (SECRET_KEY, SMTP, Stripe, etc.)

# Run server
uvicorn app.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000` — the API is live. The web frontend is served from the `www/` directory.

> 📖 For the full setup guide, see [`docs/setup.md`](docs/setup.md).

---

## 🧪 Testing

```powershell
.\.venv\Scripts\Activate.ps1
pytest test_api.py -v
```

---

## 📄 License

ISC
