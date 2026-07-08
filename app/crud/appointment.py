from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.databasemodels.models_appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


async def create_appointment(
    db: AsyncSession,
    appointment_data: AppointmentCreate,
) -> Appointment:
    appointment = Appointment(**appointment_data.model_dump())

    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)

    return appointment


async def get_appointment_by_id(
    db: AsyncSession,
    appointment_id: int,
) -> Appointment | None:
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    return result.scalar_one_or_none()


async def get_appointments(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[Appointment]:
    result = await db.execute(select(Appointment).offset(skip).limit(limit))
    return list(result.scalars().all())


async def update_appointment(
    db: AsyncSession,
    appointment: Appointment,
    appointment_data: AppointmentUpdate,
) -> Appointment:
    update_data = appointment_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(appointment, field, value)

    await db.commit()
    await db.refresh(appointment)

    return appointment


async def delete_appointment(
    db: AsyncSession,
    appointment: Appointment,
) -> None:
    await db.delete(appointment)
    await db.commit()
