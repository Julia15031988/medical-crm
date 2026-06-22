import enum
from src.database.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    Enum,
    UniqueConstraint,
)

class UserRoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"


class GenderEnum(enum.Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"


class AppointmentStatusEnum(enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRoleEnum, name="user_roles"))
    is_active = Column(Boolean, default=True)
    first_name = Column(String(50))
    last_name = Column(String(50))

    activation_token = relationship(
        "ActivationToken",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    password_reset_token = relationship(
        "PasswordResetToken",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )

    doctor_profile = relationship("DoctorProfile", uselist=False, back_populates="user")
    patient_profile = relationship("PatientProfile", uselist=False, back_populates="user")


class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    specialization = Column(String(100))
    years_experience = Column(Integer)
    hospital_branch = Column(String(100))
    phone_number = Column(String(20))

    user = relationship("User", back_populates="doctor_profile")
    appointments = relationship("Appointment", back_populates="doctor")


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    date_of_birth = Column(DateTime)
    insurance_provider = Column(String(100))
    insurance_number = Column(String(50))
    address = Column(String(255))
    gender = Column(Enum(GenderEnum, name="genders"))

    user = relationship("User", back_populates="patient_profile")
    appointments = relationship("Appointment", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient_profiles.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    reason_for_visit = Column(String(255))
    status = Column(Enum(AppointmentStatusEnum, name="appointment_status"), default=AppointmentStatusEnum.SCHEDULED)
    notes = Column(Text)

    patient = relationship("PatientProfile", back_populates="appointments")
    doctor = relationship("DoctorProfile", back_populates="appointments")


class ActivationToken(Base):
    __tablename__ = "activation_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="activation_token")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="password_reset_token")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="refresh_tokens")
