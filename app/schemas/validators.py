"""
Общие валидаторы для Pydantic схем.
"""

import re
from typing import Optional
from pydantic import field_validator, EmailStr
from email_validator import validate_email as validate_email_lib, EmailNotValidError


# ============ ВАЛИДАЦИЯ ЦВЕТА ============


def validate_hex_color(color: str) -> str:
    """
    Валидация HEX цвета формата #RRGGBB.

    Примеры валидных значений:
    - #FF5733
    - #000000
    - #FFFFFF

    Примеры невалидных:
    - FF5733      (нет #)
    - #FF5        (мало символов)
    - #GGGGGG     (не hex символы)
    """
    if not re.match(r"^#[0-9A-Fa-f]{6}$", color):
        raise ValueError("Цвет должен быть в HEX формате (#RRGGBB)")
    return color


def validate_optional_hex_color(color: Optional[str]) -> Optional[str]:
    """Валидация опционального HEX цвета"""
    if color is None:
        return color
    return validate_hex_color(color)


class ColorValidatorMixin:
    """Миксин для добавления валидации цвета в схемы"""

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        return validate_hex_color(v)

    @field_validator("color", mode="before")
    @classmethod
    def validate_optional_color(cls, v: Optional[str]) -> Optional[str]:
        return validate_optional_hex_color(v)


# ============ ВАЛИДАЦИЯ EMAIL ============


def validate_email(email: str) -> str:
    """
    Валидация email адреса.
    Использует библиотеку email-validator для надежной проверки.

    Примеры валидных:
    - user@example.com
    - first.last@domain.co.uk

    Примеры невалидных:
    - user@.com
    - @example.com
    - user@domain
    """
    try:
        # Используем библиотеку для надежной проверки
        validated = validate_email_lib(email, check_deliverability=False)
        return validated.email
    except EmailNotValidError as e:
        raise ValueError(f"Некорректный email адрес: {str(e)}")


def validate_optional_email(email: Optional[str]) -> Optional[str]:
    """Валидация опционального email"""
    if email is None:
        return email
    return validate_email(email)


class EmailValidatorMixin:
    """Миксин для валидации email"""

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return validate_email(v)

    @field_validator("email", mode="before")
    @classmethod
    def validate_optional_email(cls, v: Optional[str]) -> Optional[str]:
        return validate_optional_email(v)


# ============ ВАЛИДАЦИЯ ПАРОЛЯ (на будущее) ============


def validate_password(password: str, min_length: int = 8) -> str:
    """
    Валидация пароля.

    Требования:
    - Минимум min_length символов
    - Хотя бы одна цифра
    - Хотя бы одна буква
    """
    if len(password) < min_length:
        raise ValueError(f"Пароль должен содержать минимум {min_length} символов")

    if not any(char.isdigit() for char in password):
        raise ValueError("Пароль должен содержать хотя бы одну цифру")

    if not any(char.isalpha() for char in password):
        raise ValueError("Пароль должен содержать хотя бы одну букву")

    return password


# ============ ВАЛИДАЦИЯ НОМЕРА ТЕЛЕФОНА (на будущее) ============


def validate_phone(phone: str) -> str:
    """
    Валидация номера телефона.
    Принимает различные форматы и нормализует.

    Примеры валидных:
    - +7 (900) 123-45-67
    - 89001234567
    - 8-900-123-45-67
    """
    # Убираем все нецифровые символы
    digits = re.sub(r"\D", "", phone)

    # Проверяем российские номера
    if digits.startswith("7") or digits.startswith("8"):
        if len(digits) == 11:
            return f"+7{digits[1:]}"
        elif len(digits) == 10:
            return f"+7{digits}"

    # Проверяем международные номера
    if digits.startswith("1") and len(digits) == 11:  # США/Канада
        return f"+{digits}"

    raise ValueError("Некорректный номер телефона")


# ============ УТИЛИТЫ ДЛЯ ВАЛИДАЦИИ ============


def validate_range(value: float, min_val: float, max_val: float) -> float:
    """Проверяет что значение в диапазоне"""
    if not min_val <= value <= max_val:
        raise ValueError(f"Значение должно быть между {min_val} и {max_val}")
    return value


def validate_length(text: str, min_len: int = 1, max_len: int = 255) -> str:
    """Проверяет длину строки"""
    if len(text) < min_len:
        raise ValueError(f"Текст должен содержать минимум {min_len} символов")
    if len(text) > max_len:
        raise ValueError(f"Текст должен содержать максимум {max_len} символов")
    return text
