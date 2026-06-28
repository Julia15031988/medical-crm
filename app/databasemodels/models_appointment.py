import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databasemodels.base import Base


class AppointmentStatusEnum(enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patient_profiles.patient_id"),
        nullable=False,
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctor_profiles.doctor_id"),
        nullable=False,
    )

    appointment_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    reason_for_visit: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[AppointmentStatusEnum] = mapped_column(
        Enum(AppointmentStatusEnum, name="appointment_status"),
        default=AppointmentStatusEnum.SCHEDULED,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    patient: Mapped["PatientProfile"] = relationship(
        "PatientProfile",
        back_populates="appointments",
    )

    doctor: Mapped["DoctorProfile"] = relationship(
        "DoctorProfile",
        back_populates="appointments",
    )
