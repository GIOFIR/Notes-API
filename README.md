# Notes API

A secure RESTful API for managing personal notes, built with FastAPI and PostgreSQL, featuring JWT-based authentication and owner-based authorization.

## Features

### Authentication & Security

- User registration and login
- Secure password hashing using bcrypt
- JWT-based authentication (stateless)
- OAuth2 Password Flow (Swagger-compatible)
- Protected endpoints using dependency-based authentication

### Authorization

Owner-based authorization: Each user can access only their own notes
Unauthorized access attempts return safe 404 responses (no data leakage)

### Notes Management

Create, read, update, and delete personal notes

Notes attributes:
title, description, completed status, priority

Partial updates via PATCH

Full replacement via PUT

### Infrastructure

- PostgreSQL with async access (asyncpg)
- Custom migration system
- Exception handling
- Health check endpoint
- CORS middleware for frontend integration

## Tech Stack

- Python 3.12+
- FastAPI
- PostgreSQL
- asyncpg (async PostgreSQL driver)
- Pydantic v2
- JWT (python-jose)
- bcrypt / passlib


## Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-directory>
```
2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Setup .env file
```bash
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>

JWT_SECRET_KEY=<your-long-random-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
5. Run database migrations
```bash
python database/migrations.py migrate
```

---- Running the API ----
```bash
uvicorn main:app --reload
```
The API will run on: http://127.0.0.1:8000

Swagger docs: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/test-db

### Authentication Flow
Register : POST /auth/register
Login : POST /auth/login
Returns : 
```bash
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```
### Authorized Requests
All protected endpoints require:
```bash
Authorization: Bearer <JWT>
```
Swagger UI supports OAuth2 Password Flow via the Authorize button.

### Filtering & Search Examples

GET /notes?completed=true  
GET /notes?priority=high  
GET /notes?search=meeting  
GET /notes?completed=false&priority=medium

---

API Endpoints:
Notes
Method	Endpoint	Description
GET     /notes/all-notes	Get all user notes
GET     /notes/{note_id}	Get a specific note
POST	/notes/	            Create a new note
PUT	    /notes/{note_id}	Replace an existing note
PATCH	/notes/{note_id}	Update an existing note partially
DELETE	/notes/{note_id}	Delete a note
GET	    /test-db	        Check database connection

---

Exception Handling:
401 Unauthorized (invalid or missing token)
404 Not Found: When a note is not found.
422 Validation error
500 Internal Server Error: When there is a database error.


## License

MIT License