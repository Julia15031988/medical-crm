from datetime import date, time

from pydantic import BaseModel

from app.databasemodels.models_appointment import AppointmentStatusEnum


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: AppointmentStatusEnum = AppointmentStatusEnum.SCHEDULED
    reason: str


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: int | None = None
    doctor_id: int | None = None
    appointment_date: date | None = None
    appointment_time: time | None = None
    status: AppointmentStatusEnum | None = None
    reason: str | None = None


class AppointmentResponse(AppointmentBase):
    id: int

    model_config = {"from_attributes": True}
