from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.databasemodels.models_doctor import DoctorProfile
from app.schemas.doctor import DoctorCreate, DoctorUpdate


async def create_doctor(
    db: AsyncSession,
    doctor_data: DoctorCreate,
) -> DoctorProfile:
    doctor = DoctorProfile(**doctor_data.model_dump())

    db.add(doctor)
    await db.commit()
    await db.refresh(doctor)

    return doctor


async def get_doctor_by_id(
    db: AsyncSession,
    doctor_id: int,
) -> DoctorProfile | None:
    result = await db.execute(
        select(DoctorProfile).where(DoctorProfile.id == doctor_id)
    )
    return result.scalar_one_or_none()


async def get_doctor_by_email(
    db: AsyncSession,
    email: str,
) -> DoctorProfile | None:
    result = await db.execute(
        select(DoctorProfile).where(DoctorProfile.email == email)
    )
    return result.scalar_one_or_none()


async def get_doctors(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[DoctorProfile]:
    result = await db.execute(select(DoctorProfile).offset(skip).limit(limit))
    return list(result.scalars().all())


async def update_doctor(
    db: AsyncSession,
    doctor: DoctorProfile,
    doctor_data: DoctorUpdate,
) -> DoctorProfile:
    update_data = doctor_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(doctor, field, value)

    await db.commit()
    await db.refresh(doctor)

    return doctor


async def delete_doctor(
    db: AsyncSession,
    doctor: DoctorProfile,
) -> None:
    await db.delete(doctor)
    await db.commit()
