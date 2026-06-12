# auth.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib
import base64
import os
pwd_context        = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM          = "HS256"
TOKEN_EXPIRE_HOURS = 24

def _prepare_password(plain_password: str) -> str:
    hashed = hashlib.sha256(plain_password.encode()).digest()
    return base64.b64encode(hashed).decode()

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(_prepare_password(plain_password))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_prepare_password(plain_password), hashed_password)

def create_token(user_id: int, email: str, role: str) -> str:
    expire  = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "sub":   str(user_id),
        "email": email,
        "role":  role,
        "exp":   expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": int(payload.get("sub")),
            "email":   payload.get("email"),
            "role":    payload.get("role"),
        }
    except JWTError:
        return None