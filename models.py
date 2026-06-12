# models.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# ── User schemas ───────────────────────────────────────
class UserRegister(BaseModel):
    name:     str = Field(min_length=2, max_length=100)
    email:    EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class UserOut(BaseModel):
    id:         int
    name:       str
    email:      str
    role:       str
    is_active:  bool
    created_at: str
    model_config = {"from_attributes": True}

class TokenOut(BaseModel):
    access_token: str
    token_type:   str = "bearer"

# ── Note schemas ───────────────────────────────────────
class NoteCreate(BaseModel):
    title:   str  = Field(min_length=1, max_length=100)
    content: str  = Field(min_length=1)
    pinned:  bool = False
    tag:     Literal["work", "personal", "idea", "other"] = "other"

class NoteUpdate(BaseModel):
    title:   Optional[str]  = Field(None, min_length=1, max_length=100)
    content: Optional[str]  = Field(None, min_length=1)
    pinned:  Optional[bool] = None
    tag:     Optional[Literal["work", "personal", "idea", "other"]] = None

class NoteOut(BaseModel):
    id:         int
    title:      str
    content:    str
    pinned:     bool
    tag:        str
    owner_id:   int
    created_at: str
    updated_at: str
    model_config = {"from_attributes": True}

class NoteList(BaseModel):
    total: int
    notes: list[NoteOut]