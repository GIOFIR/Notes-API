from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from asyncpg import Pool

from database.database import get_db_pool
from auth.schemas import RegisterRequest, RegisterResponse, TokenResponse
from auth.service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    pool: Pool = Depends(get_db_pool),
):
    return await register_user(pool, payload)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    pool: Pool = Depends(get_db_pool),
):
    return await login_user(
        pool=pool,
        email=form_data.username,
        password=form_data.password,
    )
