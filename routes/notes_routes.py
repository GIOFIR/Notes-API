# notes_routes
import logging
from typing import List
from fastapi import APIRouter, HTTPException, status
from schemas.notes_schemas import NoteResponse, NoteCreate, NotePut, NotePatch
from routes.crud import get_note_by_id, get_all_notes, create_new_note, replace_note, delete_note, update_note

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/all-notes", response_model=List[NoteResponse])
async def get_note():
    """Get a specific note"""
    return await get_all_notes()

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    """Get a specific note"""
    return await get_note_by_id(note_id)
    
@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate):
    """Create a new note"""
    try:
        new_note = await create_new_note(note)
        logger.info(f"Note created: {note.title}")
        return new_note
    except Exception as e:
        logger.error(f"Note creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note creation failed"
        )
    
@router.put("/{note_id}", response_model=NoteResponse)
async def put_note(note_id: int,note_put: NotePut):
    """Replace a note (PUT operation)"""
    return await replace_note(note_id, note_put)

@router.patch("/{note_id}", response_model=NoteResponse)
async def patch_note(note_id: int,note_update: NotePatch):
    """Update a note (PATCH operation)"""
    return await update_note(note_id, note_update)

@router.delete("/{note_id}")
async def delete_note_endpoint(note_id: int):
    """Delete a note"""
    return await delete_note(note_id)
