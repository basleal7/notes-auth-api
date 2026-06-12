# routers/notes.py
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
import database as db
from models import NoteCreate, NoteUpdate, NoteOut, NoteList
from routers.users import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])

# ── GET /notes — only YOUR notes ──────────────────────
@router.get("", response_model=NoteList)
async def list_notes(
    pinned: Optional[bool] = Query(None),
    tag:    Optional[str]  = Query(None),
    current_user: dict     = Depends(get_current_user),
):
    notes = db.get_notes_by_owner(current_user["id"])

    if pinned is not None:
        notes = [n for n in notes if n["pinned"] == pinned]
    if tag:
        notes = [n for n in notes if n["tag"] == tag]

    return {"total": len(notes), "notes": notes}

# ── GET /notes/{id} ───────────────────────────────────
@router.get("/{note_id}", response_model=NoteOut)
async def get_note(
    note_id: int,
    current_user: dict = Depends(get_current_user)
):
    note = db.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your note")
    return note

# ── POST /notes — creates note owned by YOU ───────────
@router.post("", response_model=NoteOut, status_code=201)
async def create_note(
    note: NoteCreate,
    current_user: dict = Depends(get_current_user)
):
    data = note.model_dump()
    data["owner_id"] = current_user["id"]   # ← attach owner
    return db.create_note(data)

# ── PATCH /notes/{id} — only YOUR notes ───────────────
@router.patch("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int,
    changes: NoteUpdate,
    current_user: dict = Depends(get_current_user)
):
    note = db.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your note")
    return db.update_note(note_id, changes.model_dump(exclude_unset=True))

# ── DELETE /notes/{id} — only YOUR notes ──────────────
@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    current_user: dict = Depends(get_current_user)
):
    note = db.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your note")
    db.delete_note(note_id)