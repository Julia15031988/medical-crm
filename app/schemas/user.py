from pydantic import BaseModel, field_validator, EmailStr
from app.databasemodels.validators.accountsvalidators import validate_password_strength
from app.databasemodels.modelsauth import UserRoleEnum


class BaseEmailPasswordSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        return value.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return validate_password_strength(value)


# --- Signup ---
class UserRegistrationRequestSchema(BaseEmailPasswordSchema):
    role: UserRoleEnum = UserRoleEnum.PATIENT   # пацієнт реєструється сам


class UserRegistrationResponseSchema(BaseModel):
    id: int
    email: EmailStr
    role: UserRoleEnum
    is_active: bool

    model_config = {"from_attributes": True}


# --- Login ---
class UserLoginRequestSchema(BaseEmailPasswordSchema):
    pass


class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# --- Logout ---
class UserLogoutRequestSchema(BaseModel):
    refresh_token: str


# --- Change password ---
class UserChangePasswordRequestSchema(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        return validate_password_strength(value)


# --- Reset password ---
class PasswordResetRequestSchema(BaseModel):
    email: EmailStr


class PasswordResetCompleteRequestSchema(BaseModel):
    token: str
    email: EmailStr
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        return validate_password_strength(value)


# --- Token refresh ---
class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str


class TokenRefreshResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Messages ---
class MessageResponseSchema(BaseModel):
    message: str


class ResendActivationRequestSchema(BaseModel):
    email: EmailStr
