from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databasemodels.base import Base


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
