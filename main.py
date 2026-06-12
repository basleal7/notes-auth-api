# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
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

app.include_router(users.router)
app.include_router(notes.router)

@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok"}