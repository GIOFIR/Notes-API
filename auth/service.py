from fastapi import HTTPException, status
from asyncpg import Pool

from auth.users_handle import get_user_by_email, create_user
from auth.security import hash_password, verify_password
from auth.jwt import create_access_token
from auth.schemas import RegisterRequest, TokenResponse


async def register_user(pool: Pool, payload: RegisterRequest):
    existing = await get_user_by_email(pool, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    hashed_password = hash_password(payload.password)
    user = await create_user(pool, payload.email, hashed_password)
    return user


async def login_user(pool: Pool, email: str, password: str) -> TokenResponse:
    user = await get_user_by_email(pool, email)

    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=str(user["id"]))
    return TokenResponse(access_token=token)
