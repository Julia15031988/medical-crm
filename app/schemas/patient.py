from datetime import date

from pydantic import BaseModel

from app.databasemodels.models_patient import GenderEnum


class PatientBase(BaseModel):
    full_name: str
    phone: str
    gender: GenderEnum
    date_of_birth: date
    address: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    gender: GenderEnum | None = None
    date_of_birth: date | None = None
    address: str | None = None


class PatientResponse(PatientBase):
    id: int

    model_config = {"from_attributes": True}
