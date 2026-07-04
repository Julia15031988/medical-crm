from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from sqlalchemy import Enum, ForeignKey, Integer, String
from app.databasemodels.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.databasemodels.models_auth import User
    from app.databasemodels.models_appointment import Appointment


class EmploymentTypeEnum(enum.Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    specialization: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(
        Enum(EmploymentTypeEnum, name="employment_type"),
        nullable=False,
        default=EmploymentTypeEnum.FULL_TIME,
    )

    years_experience: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    hospital_branch: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="doctor_profile",
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="doctor",
    )
