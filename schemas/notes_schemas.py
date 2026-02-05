# notes_schemas
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
