# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from typing import Optional, List
from db_models import Base, UserModel, NoteModel
from auth import hash_password, verify_password

import os
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/notes_auth_db")

engine       = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()

# ── User functions ─────────────────────────────────────

def get_user_by_id(user_id: int) -> Optional[dict]:
    session = get_session()
    try:
        user = session.query(UserModel).filter(UserModel.id == user_id).first()
        return _user_to_dict(user) if user else None
    finally:
        session.close()

def get_user_by_email(email: str) -> Optional[dict]:
    session = get_session()
    try:
        user = session.query(UserModel).filter(UserModel.email == email).first()
        return _user_to_dict(user) if user else None
    finally:
        session.close()

def get_all_users() -> List[dict]:
    session = get_session()
    try:
        users = session.query(UserModel).all()
        return [_user_to_dict(u) for u in users]
    finally:
        session.close()

def create_user(data: dict) -> dict:
    session = get_session()
    try:
        data["password"] = hash_password(data["password"])
        user = UserModel(**data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return _user_to_dict(user)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def authenticate_user(email: str, password: str) -> Optional[dict]:
    session = get_session()
    try:
        user = session.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return _user_to_dict(user)
    finally:
        session.close()

# ── Note functions ─────────────────────────────────────

def get_notes_by_owner(owner_id: int) -> List[dict]:
    session = get_session()
    try:
        notes = session.query(NoteModel).filter(
            NoteModel.owner_id == owner_id
        ).all()
        return [_note_to_dict(n) for n in notes]
    finally:
        session.close()

def get_note_by_id(note_id: int) -> Optional[dict]:
    session = get_session()
    try:
        note = session.query(NoteModel).filter(NoteModel.id == note_id).first()
        return _note_to_dict(note) if note else None
    finally:
        session.close()

def create_note(data: dict) -> dict:
    session = get_session()
    try:
        note = NoteModel(**data)
        session.add(note)
        session.commit()
        session.refresh(note)
        return _note_to_dict(note)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_note(note_id: int, changes: dict) -> dict:
    session = get_session()
    try:
        note = session.query(NoteModel).filter(NoteModel.id == note_id).first()
        for key, value in changes.items():
            setattr(note, key, value)
        note.updated_at = datetime.now(timezone.utc).isoformat()
        session.commit()
        session.refresh(note)
        return _note_to_dict(note)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete_note(note_id: int) -> None:
    session = get_session()
    try:
        note = session.query(NoteModel).filter(NoteModel.id == note_id).first()
        session.delete(note)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# ── Private helpers ────────────────────────────────────

def _user_to_dict(user: UserModel) -> dict:
    return {
        "id":         user.id,
        "name":       user.name,
        "email":      user.email,
        "password":   user.password,
        "role":       user.role,
        "is_active":  user.is_active,
        "created_at": user.created_at,
    }

def _note_to_dict(note: NoteModel) -> dict:
    return {
        "id":         note.id,
        "title":      note.title,
        "content":    note.content,
        "pinned":     note.pinned,
        "tag":        note.tag,
        "owner_id":   note.owner_id,
        "created_at": note.created_at,
        "updated_at": note.updated_at,
    }