import argparse
import asyncio
import getpass
import sys

from sqlalchemy import select

from app.databasemodels.sessions import AsyncSessionLocal
from app.databasemodels.models_auth import User, UserRoleEnum
from app.databasemodels.models_doctor import DoctorProfile  # noqa: F401
from app.databasemodels.models_patient import PatientProfile  # noqa: F401
from app.databasemodels.models_appointment import Appointment  # noqa: F401
from app.security.passwords import hash_password


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create initial admin user.")
    parser.add_argument(
        "--email",
        required=True,
        help="Admin email.",
    )
    parser.add_argument(
        "--first-name",
        default="Admin",
        help="Admin first name.",
    )
    parser.add_argument(
        "--last-name",
        default="User",
        help="Admin last name.",
    )
    return parser.parse_args()


async def create_initial_admin(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"User with email {email} already exists.")
            return

        admin = User(
            email=email,
            hashed_password=hash_password(password),
            role=UserRoleEnum.ADMIN,
            is_active=True,
            first_name=first_name,
            last_name=last_name,
        )

        session.add(admin)
        await session.commit()

        print(f"Initial admin {email} created successfully.")


def main() -> None:
    args = parse_args()

    password = getpass.getpass("Enter admin password: ")
    password_confirm = getpass.getpass("Confirm admin password: ")

    if password != password_confirm:
        print("Passwords do not match.")
        sys.exit(1)

    try:
        validate_password(password)
    except ValueError as error:
        print(error)
        sys.exit(1)

    asyncio.run(
        create_initial_admin(
            email=args.email,
            password=password,
            first_name=args.first_name,
            last_name=args.last_name,
        )
    )


if __name__ == "__main__":
    main()
