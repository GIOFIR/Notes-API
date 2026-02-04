import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query

from schemas.notes_schemas import NoteResponse, NoteCreate, NotePut, NotePatch
from auth.dependencies import get_current_user
from routes.notes_service import (
    list_notes_service,
    get_note_service,
    create_note_service,
    put_note_service,
    patch_note_service,
    delete_note_service,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/notes", response_model=List[NoteResponse])
async def list_notes(
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
):
    return await list_notes_service(
        owner_id=current_user["id"],
        completed=completed,
        priority=priority,
        search=search,
    )


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user=Depends(get_current_user),
):
    return await get_note_service(note_id, owner_id=current_user["id"])


@router.post("/", response_model=NoteResponse, status_code=201)
async def create_note(
    note: NoteCreate,
    current_user=Depends(get_current_user),
):
    return await create_note_service(note, owner_id=current_user["id"])


@router.put("/{note_id}", response_model=NoteResponse)
async def put_note(
    note_id: int,
    note_put: NotePut,
    current_user=Depends(get_current_user),
):
    return await put_note_service(note_id, note_put, owner_id=current_user["id"])


@router.patch("/{note_id}", response_model=NoteResponse)
async def patch_note(
    note_id: int,
    note_update: NotePatch,
    current_user=Depends(get_current_user),
):
    return await patch_note_service(note_id, note_update, owner_id=current_user["id"])


@router.delete("/{note_id}")
async def delete_note_endpoint(
    note_id: int,
    current_user=Depends(get_current_user),
):
    return await delete_note_service(note_id, owner_id=current_user["id"])
