from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configuration.dependencies import (
    get_db,
    only_admin,
    only_doctor_or_admin,
)
from app.crud.doctor import (
    create_doctor,
    delete_doctor,
    get_doctor_by_email,
    get_doctor_by_id,
    get_doctors,
    update_doctor,
)
from app.schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdate


router = APIRouter(
    prefix="/api/v1/doctors",
    tags=["Doctors"],
)


@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_doctor_profile(
    doctor_data: DoctorCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_admin),
):
    existing_doctor = await get_doctor_by_email(db, doctor_data.email)

    if existing_doctor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doctor with this email already exists.",
        )

    return await create_doctor(db, doctor_data)


@router.get(
    "/",
    response_model=list[DoctorResponse],
)
async def read_doctors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_doctor_or_admin),
):
    return await get_doctors(db, skip, limit)


@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse,
)
async def read_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_doctor_or_admin),
):
    doctor = await get_doctor_by_id(db, doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found.",
        )

    return doctor


@router.patch(
    "/{doctor_id}",
    response_model=DoctorResponse,
)
async def update_doctor_profile(
    doctor_id: int,
    doctor_data: DoctorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_admin),
):
    doctor = await get_doctor_by_id(db, doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found.",
        )

    return await update_doctor(db, doctor, doctor_data)


@router.delete(
    "/{doctor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_doctor_profile(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_admin),
):
    doctor = await get_doctor_by_id(db, doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found.",
        )

    await delete_doctor(db, doctor)
