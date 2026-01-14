from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime
from app.schemas.validators import ColorValidatorMixi


class CategoryBase(BaseModel, ColorValidatorMixin):
    """
    Базовая схема для категории.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Название категории (2-50 символов)",
        examples=["Еда", "Транспорт"],
    )

    color: str = Field(
        default="#000000",
        description="Цвет категории в формате HEX (#RRGGBB)",
        examples=["#FF5733", "#33FF57"],
    )


class CategoryCreate(CategoryBase):
    """Схема для создания категории"""

    pass


class CategoryUpdate(BaseModel):
    """Схема для обновления категории"""

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
        description="Новое название категории",
    )

    color: Optional[str] = Field(default=None, description="Новый цвет категории")

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        from app.schemas.validators import validate_optional_hex_color

        return validate_optional_hex_color(v)


class Category(CategoryBase):
    """Схема для чтения категории (ответ API)"""

    id: str = Field(..., description="Уникальный идентификатор категории")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    model_config = ConfigDict(from_attributes=True)


__all__ = ["CategoryBase", "CategoryCreate", "CategoryUpdate", "Category"]
