import logging
from typing import Optional

from routes.crud import (
    create_new_note,
    delete_note,
    get_all_notes,
    get_note_by_id,
    replace_note,
    update_note,
)
from schemas.notes_schemas import NoteCreate, NotePatch, NotePut

logger = logging.getLogger(__name__)

async def list_notes_service(
    owner_id: int,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
):
    return await get_all_notes(
        owner_id=owner_id,
        completed=completed,
        priority=priority,
        search=search,
    )

async def get_note_service(note_id: int, owner_id: int):
    return await get_note_by_id(note_id, owner_id=owner_id)

async def create_note_service(note: NoteCreate, owner_id: int):
    new_note = await create_new_note(note, owner_id=owner_id)
    logger.info(f"Note created for user {owner_id}: {note.title}")
    return new_note

async def put_note_service(note_id: int, note_put: NotePut, owner_id: int):
    return await replace_note(note_id, note_put, owner_id=owner_id)

async def patch_note_service(note_id: int, note_patch: NotePatch, owner_id: int):
    return await update_note(note_id, note_patch, owner_id=owner_id)

async def delete_note_service(note_id: int, owner_id: int):
    return await delete_note(note_id, owner_id=owner_id)
