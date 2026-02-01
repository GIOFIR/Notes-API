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
    priority: str

class NotePatch(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str 

class NoteResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str 
    created_at: datetime
    updated_at: Optional[datetime] = None
