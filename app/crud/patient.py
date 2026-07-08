from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.databasemodels.models_patient import PatientProfile
from app.schemas.patient import PatientCreate, PatientUpdate


async def create_patient(
    db: AsyncSession,
    patient_data: PatientCreate,
) -> PatientProfile:
    patient = PatientProfile(**patient_data.model_dump())

    db.add(patient)
    await db.commit()
    await db.refresh(patient)

    return patient


async def get_patient_by_id(
    db: AsyncSession,
    patient_id: int,
) -> PatientProfile | None:
    result = await db.execute(
        select(PatientProfile).where(PatientProfile.id == patient_id)
    )
    return result.scalar_one_or_none()


async def get_patients(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[PatientProfile]:
    result = await db.execute(select(PatientProfile).offset(skip).limit(limit))
    return list(result.scalars().all())


async def update_patient(
    db: AsyncSession,
    patient: PatientProfile,
    patient_data: PatientUpdate,
) -> PatientProfile:
    update_data = patient_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(patient, field, value)

    await db.commit()
    await db.refresh(patient)

    return patient


async def delete_patient(
    db: AsyncSession,
    patient: PatientProfile,
) -> None:
    await db.delete(patient)
    await db.commit()
