import logging
from database.database import get_db_pool
from exceptions.custom_exceptions import NoteNotFoundError, DatabaseError
from schemas.notes_schemas import NoteResponse, NoteCreate, NotePut, NotePatch

logger = logging.getLogger(__name__)

async def get_note_by_id(note_id: int):
    """Get note by note id or raise exception if not found"""
    pool = get_db_pool()
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow('SELECT * FROM notes WHERE id = $1', note_id)
            if row is None:
                raise NoteNotFoundError(note_id)
            return NoteResponse(**row)
        
        except Exception as e:
            if isinstance(e, NoteNotFoundError):
                        raise
            logger.error(f"Database error while fetching NOTE {note_id}: {str(e)}")
            raise DatabaseError(f"Failed to fetch NOTE: {str(e)}")

async def get_all_notes():
    """Get all notes """
    pool = get_db_pool()
    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch('SELECT * FROM notes')
            if rows is None:
                raise NoteNotFoundError()
            return [NoteResponse(**row) for row in rows]
        
        except Exception as e:
            if isinstance(e, NoteNotFoundError):
                        raise
            logger.error(f"Database error while fetching notes : {str(e)}")
            raise DatabaseError(f"Failed to fetch notes: {str(e)}")

async def create_new_note(note: NoteCreate) -> NoteResponse:
    """Create a new note"""
    pool = get_db_pool()
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow('''
                INSERT INTO notes (title, description)
                VALUES ($1, $2)
                RETURNING id, title, description, completed, created_at
            ''', note.title, note.description)
            return NoteResponse(**row)
        except Exception as e:
            logger.error(f"Database error while creating note for user: {str(e)}")
            raise DatabaseError(f"Failed to create note: {str(e)}")
        
async def replace_note(note_id: int, data: NotePut) -> NoteResponse:
    """Replace a note (PUT operation)"""
    pool = get_db_pool()
    async with pool.acquire() as conn:
        try:
            # Ensure note exists
            existing_note = await conn.fetchrow("SELECT id FROM notes WHERE id = $1", note_id)
            if not existing_note:
                raise NoteNotFoundError(f"Note {note_id} not found")
            
            updated_row = await conn.fetchrow(
                '''
                UPDATE notes
                SET title = $1, description = $2, completed = $3
                WHERE id = $4 
                RETURNING id, title, description, completed, created_at
                ''',
                data.title, data.description, data.completed, note_id)
            return NoteResponse(**updated_row)
        except Exception as e:
            if isinstance(e, NoteNotFoundError):
                raise
            logger.error(f"Database error while replacing note {note_id}: {str(e)}")
            raise DatabaseError(f"Failed to update note: {str(e)}")

async def update_note(note_id: int, patch: NotePatch) -> NoteResponse:
    """Update a note (PATCH operation)"""
    pool = get_db_pool()
    async with pool.acquire() as conn:
        try:
            existing = await get_note_by_id(note_id)

            update_fields = []
            values = []
            param_count = 1

            if patch.title is not None:
                update_fields.append(f"title = ${param_count}")
                values.append(patch.title)
                param_count += 1

            if patch.description is not None:
                update_fields.append(f"description = ${param_count}")
                values.append(patch.description)
                param_count += 1

            if patch.completed is not None:
                update_fields.append(f"completed = ${param_count}")
                values.append(patch.completed)
                param_count += 1

            if not update_fields:
                return NoteResponse(**existing)

            values.extend([note_id])
            query = f"""
                UPDATE notes
                SET {', '.join(update_fields)}
                WHERE id = ${param_count}
                RETURNING id, title, description, completed, created_at
            """
            updated_row = await conn.fetchrow(query, *values)
            return NoteResponse(**updated_row)
        except Exception as e:
            if isinstance(e, NoteNotFoundError):
                raise
            logger.error(f"Database error while updating note {note_id}: {str(e)}")
            raise DatabaseError(f"Failed to update note: {str(e)}")  

async def delete_note(note_id: int) -> dict:
    """Delete a note"""
    pool = get_db_pool()
    async with pool.acquire() as conn:
        try:
            await get_note_by_id(note_id)
            
            result = await conn.execute('DELETE FROM notes WHERE id = $1 ',note_id)
            
            if result == "DELETE 0":
                raise NoteNotFoundError(note_id)
                
            logger.info(f"NOTE {note_id} deleted successfully ")
            return {"message": f"NOTE {note_id} deleted successfully"}
        except Exception as e:
            if isinstance(e, NoteNotFoundError):
                raise
            logger.error(f"Failed to delete NOTE {note_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete NOTE: {str(e)}")
