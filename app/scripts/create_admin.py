import asyncio
import os

from sqlalchemy import select

from app.databasemodels.sessions import AsyncSessionLocal
from app.databasemodels.models_auth import User, UserRoleEnum
from app.security.passwords import hash_password
from app.databasemodels.models_doctor import DoctorProfile  # noqa: F401
from app.databasemodels.models_patient import PatientProfile  # noqa: F401
from app.databasemodels.models_appointment import Appointment  # noqa: F401


async def create_admin() -> None:
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_first_name = os.getenv("ADMIN_FIRST_NAME", "Admin")
    admin_last_name = os.getenv("ADMIN_LAST_NAME", "User")

    if not admin_email or not admin_password:
        print("Admin credentials are not set. Skipping admin creation.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == admin_email))
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print("Admin already exists. Skipping admin creation.")
            return

        admin = User(
            email=admin_email,
            hashed_password=hash_password(admin_password),
            role=UserRoleEnum.ADMIN,
            is_active=True,
            first_name=admin_first_name,
            last_name=admin_last_name,
        )

        session.add(admin)
        await session.commit()

        print(f"Admin user {admin_email} created successfully.")


if __name__ == "__main__":
    asyncio.run(create_admin())
