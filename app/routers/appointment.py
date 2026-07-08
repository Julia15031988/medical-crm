from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configuration.dependencies import (
    get_db,
    only_admin,
    only_doctor_or_admin,
)
from app.crud.appointment import (
    create_appointment,
    delete_appointment,
    get_appointment_by_id,
    get_appointments,
    update_appointment,
)
from app.crud.doctor import get_doctor_by_id
from app.crud.patient import get_patient_by_id
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
)


router = APIRouter(
    prefix="/api/v1/appointments",
    tags=["Appointments"],
)


@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment_route(
    appointment_data: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_admin),
):
    patient = await get_patient_by_id(db, appointment_data.patient_id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )

    doctor = await get_doctor_by_id(db, appointment_data.doctor_id)
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found.",
        )

    return await create_appointment(db, appointment_data)


@router.get(
    "/",
    response_model=list[AppointmentResponse],
)
async def read_appointments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_doctor_or_admin),
):
    return await get_appointments(db, skip, limit)


@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
async def read_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_doctor_or_admin),
):
    appointment = await get_appointment_by_id(db, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    return appointment


@router.patch(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
async def update_appointment_route(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_admin),
):
    appointment = await get_appointment_by_id(db, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    return await update_appointment(db, appointment, appointment_data)


@router.delete(
    "/{appointment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_appointment_route(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_admin),
):
    appointment = await get_appointment_by_id(db, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    await delete_appointment(db, appointment)
