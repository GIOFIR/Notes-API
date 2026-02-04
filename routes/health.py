import logging
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from database.database import fetch_db_version

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health - Check"])

@router.get("/test-db")
async def test_database():
    try:
        version = await fetch_db_version()
        return {"status": "success", "database_version": version}
    except Exception:
        logger.exception("Health check failed")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "error", "message": "Database unavailable"},
        )
