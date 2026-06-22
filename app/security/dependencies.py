from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.databasemodels.sessions import get_db
from app.databasemodels.modelsauth import User, UserRoleEnum
from app.security.jwt_manager import jwt_manager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt_manager.decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    stmt = select(User).where(User.id == int(user_id))
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user


async def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required.")
    return current_user


async def doctor_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRoleEnum.DOCTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor privileges required.")
    return current_user


async def patient_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRoleEnum.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Patient privileges required.")
    return current_user
