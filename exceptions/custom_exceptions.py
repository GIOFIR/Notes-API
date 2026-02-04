class NoteNotFoundError(Exception):
    def __init__(self, note_id: int):
        self.note_id = note_id
        super().__init__(f"Note with id {note_id} not found")


class DatabaseError(Exception):
    pass
