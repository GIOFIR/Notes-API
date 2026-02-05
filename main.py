# main
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import router as auth_router
from database.database import close_db, init_db
from database.migrations import MigrationManager
from exceptions.handlers import register_exception_handlers
from routes.health import router as health_router
from routes.notes_routes import router as notes_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting application...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Run migrations
    try:
        migration_manager = MigrationManager()
        await migration_manager.migrate()
        logger.info("Migrations completed")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
    
    yield
    
    # Cleanup
    await close_db()
    logger.info("Application shutdown complete")

app = FastAPI(
    title="Notes API",
    description="""
    Notes API with:
    * Personal notes management
    * RESTful API design
    """,
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:8080", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(notes_router)



# Register exception handlers
register_exception_handlers(app)

@app.get("/", tags=["Root"])
async def root():
    """API Root endpoint with navigation"""
    return {
        "message": "Welcome to Notes API",
        "version": "2.0.0",
        "endpoints": {
            "documentation": "/docs",
            "health_check": "/test-db",
            "notes": "/notes",
        },
        "features": [
            "Personal notes management", 
            "RESTful API design",
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)