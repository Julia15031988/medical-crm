from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configuration.dependencies import (
    get_db,
    only_admin,
    only_doctor_or_admin,
    get_current_user,
)
from app.crud.patient import (
    create_patient,
    delete_patient,
    get_patient_by_id,
    get_patients,
    update_patient,
)
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.post(
    "/{user_id}",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_patient_profile(
    user_id: int,
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_doctor_or_admin),
):
    existing_patient = await get_patient_by_id(db, user_id)

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Patient profile already exists.",
        )

    return await create_patient(db, user_id, patient_data)


@router.get("/me", response_model=PatientResponse)
async def read_my_patient_profile(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    patient = await get_patient_by_id(db, current_user.id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found.",
        )

    return patient


@router.get(
    "/",
    response_model=list[PatientResponse],
)
async def read_patients(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_doctor_or_admin),
):
    return await get_patients(db, skip, limit)


@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
)
async def read_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_doctor_or_admin),
):
    patient = await get_patient_by_id(db, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )

    return patient


@router.patch(
    "/{patient_id}",
    response_model=PatientResponse,
)
async def update_patient_profile(
    patient_id: int,
    patient_data: PatientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_doctor_or_admin),
):
    patient = await get_patient_by_id(db, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )

    return await update_patient(db, patient, patient_data)


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_profile(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(only_admin),
):
    patient = await get_patient_by_id(db, patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )

    await delete_patient(db, patient)
