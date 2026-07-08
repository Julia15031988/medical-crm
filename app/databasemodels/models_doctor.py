from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.databasemodels.models_appointment import Appointment

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databasemodels.base import Base


class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    specialization: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    experience_years: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="doctor",
    )
