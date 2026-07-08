from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.appointment import (
    create_appointment,
    get_doctor_appointment_at_time,
)
from app.crud.doctor import get_doctor_by_id
from app.crud.patient import get_patient_by_id
from app.schemas.appointment import AppointmentCreate


async def create_appointment_with_validation(
    db: AsyncSession,
    appointment_data: AppointmentCreate,
):
    # 1. Check doctor
    doctor = await get_doctor_by_id(
        db,
        appointment_data.doctor_id,
    )

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found.",
        )

    # 2. Check patient
    patient = await get_patient_by_id(
        db,
        appointment_data.patient_id,
    )

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )

    # 3. Check appointment date
    if appointment_data.scheduled_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment must be scheduled in the future.",
        )

    # 4. Check doctor's availability
    existing = await get_doctor_appointment_at_time(
        db=db,
        doctor_id=appointment_data.doctor_id,
        scheduled_at=appointment_data.scheduled_at,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doctor already has an appointment at this time.",
        )

    # 5. Create appointment
    appointment = await create_appointment(
        db=db,
        appointment_data=appointment_data,
    )

    return appointment
