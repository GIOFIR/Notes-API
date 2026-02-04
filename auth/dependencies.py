from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from asyncpg import Pool
from database.database import get_db_pool
from auth.jwt import decode_access_token
from auth.users_handle import get_user_by_id
from auth.schemas import TokenData
from jose import JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), pool: Pool = Depends(get_db_pool)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        token_data = TokenData.model_validate(payload)
    except (JWTError, Exception):
        raise credentials_exception
    
    try:
        user_id = int(token_data.sub)
    except ValueError:
        raise credentials_exception
    
    user = await get_user_by_id(pool, user_id)
    if not user:
        raise credentials_exception

    return user

