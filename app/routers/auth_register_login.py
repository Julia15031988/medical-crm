from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.databasemodels.modelsauth import User
from app.databasemodels.sessions import get_db
from app.schemas.user import UserRegistrationRequestSchema, UserLoginRequestSchema, UserLoginResponseSchema
from app.security.token_manager import JWTAuthManager
from app.configuration.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

jwt_manager = JWTAuthManager(
    secret_key_access=settings.SECRET_KEY_ACCESS,
    secret_key_refresh=settings.SECRET_KEY_REFRESH,
    algorithm=settings.ALGORITHM,
)

# --- Registration ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegistrationRequestSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_pw = pwd_context.hash(payload.password)
    new_user = User(email=payload.email, hashed_password=hashed_pw, role=payload.role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"detail": "User registered successfully"}

# --- Login ---
@router.post("/login", response_model=UserLoginResponseSchema)
async def login(payload: UserLoginRequestSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = jwt_manager.create_access_token({"user_id": user.id})
    refresh_token = jwt_manager.create_refresh_token({"user_id": user.id})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 3600,
    }
