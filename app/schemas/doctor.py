from pydantic import BaseModel, EmailStr


class DoctorBase(BaseModel):
    full_name: str
    phone: str
    email: EmailStr
    specialization: str
    experience_years: int


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    specialization: str | None = None
    experience_years: int | None = None


class DoctorResponse(DoctorBase):
    id: int

    model_config = {"from_attributes": True}
