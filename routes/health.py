# health
from fastapi import APIRouter
from database.database import fetch_db_version

router = APIRouter(tags=["Health - Check"])

@router.get("/test-db")
async def test_database():
    try:
        version = await fetch_db_version()
        return {"status": "success", "database_version": version}
    except Exception as e:
        return {"status": "error", "message": str(e)}
