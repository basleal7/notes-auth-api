# routers/users.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import database as db
from models import UserRegister, UserLogin, UserOut, TokenOut
from auth import create_token, decode_token

router   = APIRouter(tags=["Auth"])
security = HTTPBearer()

# ── Dependency — get current user from token ───────────
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token      = credentials.credentials
    token_data = decode_token(token)

    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.get_user_by_id(token_data["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# ── POST /auth/register ────────────────────────────────
@router.post("/auth/register", response_model=UserOut, status_code=201)
async def register(user: UserRegister):
    existing = db.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db.create_user(user.model_dump())

# ── POST /auth/login ───────────────────────────────────
@router.post("/auth/login", response_model=TokenOut)
async def login(credentials: UserLogin):
    user = db.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong email or password")
    token = create_token(user["id"], user["email"], user["role"])
    return {"access_token": token, "token_type": "bearer"}

# ── GET /users/me ──────────────────────────────────────
@router.get("/users/me", response_model=UserOut)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user