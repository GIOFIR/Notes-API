from dotenv import load_dotenv
import os

# load file .env
load_dotenv()

# get the DB url
DATABASE_URL = os.getenv("DATABASE_URL")

# check exist
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")
