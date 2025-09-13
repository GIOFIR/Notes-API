# custom_exceptions
class NoteNotFoundError(Exception):
    def __init__(self, Note_id: int):
        self.Note_id = Note_id
        super().__init__(f"Note with id {Note_id} not found")

class DatabaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
