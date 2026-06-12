# db_models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(100), nullable=False, unique=True)
    password   = Column(String,      nullable=False)
    role       = Column(String(20),  default="user")
    is_active  = Column(Boolean,     default=True)
    created_at = Column(String,      default=lambda: datetime.now(timezone.utc).isoformat())

class NoteModel(Base):
    __tablename__ = "notes"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    title      = Column(String(100), nullable=False)
    content    = Column(String,      nullable=False)
    pinned     = Column(Boolean,     default=False)
    tag        = Column(String(20),  default="other")
    owner_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(String,  default=lambda: datetime.now(timezone.utc).isoformat())
    updated_at = Column(String,  default=lambda: datetime.now(timezone.utc).isoformat())