from dotenv import load_dotenv
import os

# load file .env
load_dotenv()

# get the DB url
DATABASE_URL = os.getenv("DATABASE_URL")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# check exist
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")
