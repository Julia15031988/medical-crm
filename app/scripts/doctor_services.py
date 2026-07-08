from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.doctor import create_doctor_profile, get_doctor_by_id
from app.databasemodels.models_auth import UserRoleEnum
from app.crud.auth import get_user_by_email, create_user
from app.crud.doctor import create_doctor_profile
from app.schemas.doctor import DoctorCreate


async def create_doctor_with_user(
    db: AsyncSession,
    doctor_data: DoctorCreate,
):
    existing_user = await get_user_by_email(db, doctor_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    user = await create_user(
        db=db,
        email=doctor_data.email,
        password=doctor_data.password,
        role=UserRoleEnum.DOCTOR,
    )

    user.first_name = doctor_data.first_name
    user.last_name = doctor_data.last_name

    doctor_profile = await create_doctor_profile(
        db=db,
        doctor_id=user.id,
        specialization=doctor_data.specialization,
        employment_type=doctor_data.employment_type,
        years_experience=doctor_data.years_experience,
        hospital_branch=doctor_data.hospital_branch,
        phone_number=doctor_data.phone_number,
        bio=doctor_data.bio,
    )

    await db.commit()

    doctor_with_user = await get_doctor_by_id(db, user.id)

    return doctor_with_user
docker compose up --build
