from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.databasemodels.models_auth import UserRoleEnum
from app.databasemodels.validators.accountsvalidators import (
    validate_password_strength,
)


class BaseEmailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(..., description="User email address")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return value.lower()


class BaseEmailPasswordSchema(BaseEmailSchema):
    password: str = Field(
        ...,
        min_length=8,
        description="User password",
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)


# -------------------- Registration --------------------


class UserRegistrationRequestSchema(BaseEmailPasswordSchema):
    role: UserRoleEnum = UserRoleEnum.ADMIN


class UserRegistrationResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRoleEnum
    is_active: bool


# -------------------- Login --------------------


class UserLoginRequestSchema(BaseEmailPasswordSchema):
    pass


class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# -------------------- Logout --------------------


class UserLogoutRequestSchema(BaseModel):
    refresh_token: str


# -------------------- Change password --------------------


class UserChangePasswordRequestSchema(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)


# -------------------- Password reset --------------------


class PasswordResetRequestSchema(BaseEmailSchema):
    pass


class PasswordResetCompleteRequestSchema(BaseEmailSchema):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)


# -------------------- Refresh token --------------------


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str


class TokenRefreshResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -------------------- Email activation --------------------


class ResendActivationRequestSchema(BaseEmailSchema):
    pass


# -------------------- Common responses --------------------


class MessageResponseSchema(BaseModel):
    message: str
