# Notes API

A RESTful API for managing personal notes using FastAPI and PostgreSQL.

## Features

- Create, read, update, and delete personal notes.
- Notes have attributes: title, description, completed status, and priority.
- Full database migration support.
- Health check endpoint to verify database connection.
- CORS middleware for frontend integration.

## Tech Stack

- Python 3.12+
- FastAPI
- PostgreSQL
- asyncpg (async PostgreSQL driver)
- Pydantic for data validation


## Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-directory>

2. **Create a virtual environment**

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install dependencies
pip install -r requirements.txt

4. Setup .env file
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>

5. Run database migrations
python database/migrations.py migrate

---- Running the API ----

uvicorn app.main:app --reload

The API will run on: http://127.0.0.1:8000

Swagger docs: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/test-db

API Endpoints:

Notes
Method	Endpoint	Description
GET	/notes/all-notes	Get all notes
GET	/notes/{note_id}	Get a specific note
POST	/notes/	Create a new note
PUT	/notes/{note_id}	Replace an existing note
PATCH	/notes/{note_id}	Update an existing note partially
DELETE	/notes/{note_id}	Delete a note
Health
Method	Endpoint	Description
GET	/test-db	Check database connection

Exception Handling:
404 Not Found: When a note is not found.
500 Internal Server Error: When there is a database error.

