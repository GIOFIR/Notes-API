from fastapi import APIRouter, HTTPException, status, Depends

from database.database import get_db_pool  
from schemas.auth_schemas import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, TokenResponse
from auth.users_handle import get_user_by_email, create_user
from auth.security import hash_password, verify_password  
from auth.jwt import create_access_token

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    pool = get_db_pool()

    existing = await get_user_by_email(pool, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed = hash_password(payload.password)
    user = await create_user(pool, payload.email, hashed)
    return user

# @router.post("/login", response_model=TokenResponse)
# async def login(payload: LoginRequest):
#     pool = get_db_pool()

#     user = await get_user_by_email(pool, payload.email)
#     if not user or not verify_password(payload.password, user["hashed_password"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password",
#         )

#     token = create_access_token(subject=str(user["id"]))
#     return {"access_token": token, "token_type": "bearer"}




@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pool = get_db_pool()

    # Swagger ישלח username, אז נשתמש בו כ-email
    user = await get_user_by_email(pool, form_data.username)

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=str(user["id"]))
    return {"access_token": token, "token_type": "bearer"}
