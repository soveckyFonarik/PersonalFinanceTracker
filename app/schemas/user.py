from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime
from app.schemas.validators import EmailValidatorMixin


class UserBase(BaseModel, EmailValidatorMixin):
    email: str = Field(
        ...,
        max_length=100,
        description="Email пользователя",
        examples=["user@example.com"],
    )

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Имя пользователя (3-50 символов)",
        examples=["john_doe"],
    )


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[str] = Field(
        default=None,  # ← ЕСТЬ default=None?
        max_length=100,
        description="Новый email пользователя",
    )

    username: Optional[str] = Field(
        default=None,  # ← ЕСТЬ default=None?
        min_length=3,
        max_length=50,
        description="Новое имя пользователя",
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        from app.schemas.validators import validate_optional_email

        return validate_optional_email(v)


class User(UserBase):
    id: str = Field(..., description="Уникальный идентификатор пользователя")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    model_config = ConfigDict(from_attributes=True)


__all__ = ["UserBase", "UserCreate", "UserUpdate", "User"]
