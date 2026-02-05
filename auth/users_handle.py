from typing import Any, Dict, Optional

from asyncpg import Pool


async def get_user_by_email(pool: Pool, email: str) -> Optional[Dict[str, Any]]:
    query = """
        SELECT id, email, hashed_password
        FROM users
        WHERE email = $1
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, email)
        return dict(row) if row else None

async def create_user(pool: Pool, email: str, hashed_password: str) -> Dict[str, Any]:
    query = """
        INSERT INTO users (email, hashed_password)
        VALUES ($1, $2)
        RETURNING id, email
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, email, hashed_password)
        return dict(row)

async def get_user_by_id(pool: Pool, user_id: int) -> Optional[Dict[str, Any]]:
    query = """
        SELECT id, email
        FROM users
        WHERE id = $1
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, user_id)
        return dict(row) if row else None
