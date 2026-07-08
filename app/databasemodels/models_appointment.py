import enum
from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databasemodels.base import Base

if TYPE_CHECKING:
    from app.databasemodels.models_patient import PatientProfile
    from app.databasemodels.models_doctor import DoctorProfile


class AppointmentStatusEnum(enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patient_profiles.id"),
        nullable=False,
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctor_profiles.id"),
        nullable=False,
    )

    appointment_date: Mapped[date] = mapped_column(Date, nullable=False)

    appointment_time: Mapped[time] = mapped_column(Time, nullable=False)

    status: Mapped[AppointmentStatusEnum] = mapped_column(
        Enum(AppointmentStatusEnum, name="appointment_statuses"),
        nullable=False,
        default=AppointmentStatusEnum.SCHEDULED,
    )

    reason: Mapped[str] = mapped_column(String(255), nullable=False)

    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile",
        back_populates="appointments",
    )

    doctor: Mapped["DoctorProfile"] = relationship(
        "DoctorProfile",
        back_populates="appointments",
    )
