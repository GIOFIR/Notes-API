# app/exceptions/handlers.py
import logging
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from exceptions.custom_exceptions import NoteNotFoundError, DatabaseError

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NoteNotFoundError)
    async def note_not_found_handler(request, exc: NoteNotFoundError):
        logger.warning(f"Note not found: {exc.note_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Note Not Found",
                     "message": f"Note with id {exc.note_id} does not exist"}
        )

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request, exc: DatabaseError):
        logger.error(f"Database error: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Database Error",
                     "message": "An internal database error occurred"}
        )
