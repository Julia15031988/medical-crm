import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databasemodels.base import Base


class GenderEnum(enum.Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum, name="genders"),
        nullable=False,
    )
    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="patient_profile",
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="patient",
    )
