import enum
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.databasemodels.models_doctor import DoctorProfile
    from app.databasemodels.models_patient import PatientProfile

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databasemodels.base import Base


class UserRoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, name="user_roles"),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    first_name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    last_name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    activation_token: Mapped["ActivationToken | None"] = relationship(
        "ActivationToken",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )

    password_reset_token: Mapped["PasswordResetToken | None"] = relationship(
        "PasswordResetToken",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    doctor_profile: Mapped["DoctorProfile | None"] = relationship(
        "DoctorProfile",
        uselist=False,
        back_populates="user",
    )

    patient_profile: Mapped["PatientProfile | None"] = relationship(
        "PatientProfile",
        uselist=False,
        back_populates="user",
    )


class ActivationToken(Base):
    __tablename__ = "activation_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="activation_token",
    )


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="password_reset_token",
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
    )
