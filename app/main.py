import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.routers import auth_router, wallet_router, chat_router, moderation_router, verification_router, profile_router, match_router, admin_router

os.makedirs("static/uploads", exist_ok=True)

app = FastAPI(title="Talk & Earn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"^https?://localhost:\d+|https?://127\.0\.0\.1:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router.router)
app.include_router(wallet_router.router)
app.include_router(chat_router.router)
app.include_router(moderation_router.router)
app.include_router(verification_router.router)
app.include_router(profile_router.router)
app.include_router(match_router.router)
app.include_router(admin_router.router)

# Create DB tables on startup (for demo; use Alembic in prod)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Serve the web frontend from www/ at root (must be LAST — after all API routers)
os.makedirs("www", exist_ok=True)
app.mount("/", StaticFiles(directory="www", html=True), name="www")