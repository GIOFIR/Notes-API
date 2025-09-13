# notes_schemas
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Simple schemas for notes
class NoteCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"

class NotePut(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class NotePatch(BaseModel):
    """check later for comments"""
    # id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    # user_id: int = 1
    # created_at: datetime
    # updated_at: Optional[datetime] = None

class NoteResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    user_id: int = 1
    created_at: datetime
    updated_at: Optional[datetime] = None
