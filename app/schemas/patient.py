from datetime import date

from pydantic import BaseModel, ConfigDict

from app.databasemodels.models_patient import GenderEnum


class PatientBase(BaseModel):
    gender: GenderEnum
    date_of_birth: date
    address: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    gender: GenderEnum | None = None
    date_of_birth: date | None = None
    address: str | None = None


class PatientResponse(PatientBase):
    patient_id: int

    model_config = ConfigDict(from_attributes=True)
