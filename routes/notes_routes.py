# notes_routes
import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from schemas.notes_schemas import NoteResponse, NoteCreate, NotePut, NotePatch
from routes.crud import get_note_by_id, get_all_notes, create_new_note, replace_note, delete_note, update_note
from auth.dependencies import get_current_user


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/all-notes", response_model=List[NoteResponse])
async def get_note(current_user=Depends(get_current_user)):
    """Get a specific note"""
    return await get_all_notes(owner_id=current_user["id"])


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, current_user=Depends(get_current_user)):
    note = await get_note_by_id(note_id, owner_id=current_user["id"])
    if not note:
        # בכוונה 404 כדי לא “לגלות” אם קיים פתק של מישהו אחר
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

    
@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, current_user=Depends(get_current_user)):
    """Create a new note for the authenticated user"""
    try:
        new_note = await create_new_note(note, owner_id=current_user["id"])
        logger.info(f"Note created for user {current_user['id']}: {note.title}")
        return new_note
    except Exception as e:
        logger.error(f"Note creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note creation failed"
        )

    
@router.put("/{note_id}", response_model=NoteResponse)
async def put_note(note_id: int,note_put: NotePut, current_user=Depends(get_current_user)):
    """Replace a note (PUT operation)"""
    return await replace_note(note_id, note_put, owner_id=current_user["id"])

@router.patch("/{note_id}", response_model=NoteResponse)
async def patch_note(note_id: int,note_update: NotePatch, current_user=Depends(get_current_user)):
    """Update a note (PATCH operation)"""
    return await update_note(note_id, note_update, owner_id=current_user["id"])

@router.delete("/{note_id}")
async def delete_note_endpoint(note_id: int, current_user=Depends(get_current_user)):
    """Delete a note"""
    return await delete_note(note_id, owner_id=current_user["id"])
