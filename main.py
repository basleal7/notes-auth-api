# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import notes, users
import database as db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield

app = FastAPI(
    title="Notes + Auth API",
    description="Notes API with user authentication.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS — allow frontend to talk to backend ──────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://note-app-psi-jade.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(notes.router)

@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok"}