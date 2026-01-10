"""
Тесты общих валидаторов.
"""

import pytest
from app.schemas.validators import (
    validate_hex_color,
    validate_email,
    validate_password,
    validate_phone,
    validate_range,
    validate_length,
)


class TestHexColorValidator:
    """Тесты валидации HEX цвета."""

    @pytest.mark.parametrize(
        "color,is_valid",
        [
            ("#FF5733", True),
            ("#000000", True),
            ("#123ABC", True),
            ("FF5733", False),  # нет #
            ("#12345", False),  # мало символов
            ("#GGGGGG", False),  # не hex
        ],
    )
    def test_validate_hex_color(self, color, is_valid):
        """Параметризованный тест валидации цвета."""
        if is_valid:
            result = validate_hex_color(color)
            assert result == color
        else:
            with pytest.raises(ValueError) as exc_info:
                validate_hex_color(color)
            assert "HEX" in str(exc_info.value)


class TestEmailValidator:
    """Тесты валидации email."""

    @pytest.mark.parametrize(
        "email,is_valid",
        [
            ("test@example.com", True),
            ("first.last@domain.co.uk", True),
            ("user@.com", False),
            ("@example.com", False),
            ("user@domain", False),
        ],
    )
    def test_validate_email(self, email, is_valid):
        """Параметризованный тест валидации email."""
        if is_valid:
            result = validate_email(email)
            # email-validator нормализует email
            assert "@" in result and "." in result.split("@")[-1]
        else:
            with pytest.raises(ValueError) as exc_info:
                validate_email(email)
            assert "email" in str(exc_info.value).lower()


class TestPasswordValidator:
    """Тесты валидации пароля."""

    def test_valid_password(self):
        """Тест валидного пароля."""
        password = "Password123"
        result = validate_password(password)
        assert result == password

    def test_password_too_short(self):
        """Тест слишком короткого пароля."""
        with pytest.raises(ValueError) as exc_info:
            validate_password("Short1")
        assert "минимум" in str(exc_info.value)

    def test_password_no_digits(self):
        """Тест пароля без цифр."""
        with pytest.raises(ValueError) as exc_info:
            validate_password("NoDigitsHere")
        assert "цифр" in str(exc_info.value) or "digit" in str(exc_info.value)

    def test_password_no_letters(self):
        """Тест пароля без букв."""
        with pytest.raises(ValueError) as exc_info:
            validate_password("12345678")
        assert "букв" in str(exc_info.value) or "letter" in str(exc_info.value)


class TestPhoneValidator:
    """Тесты валидации номера телефона."""

    @pytest.mark.parametrize(
        "phone,expected",
        [
            ("+7 (900) 123-45-67", "+79001234567"),
            ("89001234567", "+79001234567"),
            ("8-900-123-45-67", "+79001234567"),
            ("+1-800-123-4567", "+18001234567"),  # США
        ],
    )
    def test_valid_phone_numbers(self, phone, expected):
        """Тест валидных номеров телефона."""
        result = validate_phone(phone)
        assert result == expected

    def test_invalid_phone_number(self):
        """Тест невалидного номера телефона."""
        with pytest.raises(ValueError) as exc_info:
            validate_phone("12345")
        assert "номер" in str(exc_info.value).lower()


class TestUtilityValidators:
    """Тесты утилитных валидаторов."""

    def test_validate_range(self):
        """Тест проверки диапазона."""
        # Валидное значение
        result = validate_range(5, 1, 10)
        assert result == 5

        # Ниже диапазона
        with pytest.raises(ValueError) as exc_info:
            validate_range(0, 1, 10)
        assert "между" in str(exc_info.value)

        # Выше диапазона
        with pytest.raises(ValueError) as exc_info:
            validate_range(11, 1, 10)
        assert "между" in str(exc_info.value)

    def test_validate_length(self):
        """Тест проверки длины строки."""
        # Валидная строка
        result = validate_length("Hello", 2, 10)
        assert result == "Hello"

        # Слишком короткая
        with pytest.raises(ValueError) as exc_info:
            validate_length("H", 2, 10)
        assert "минимум" in str(exc_info.value)

        # Слишком длинная
        with pytest.raises(ValueError) as exc_info:
            validate_length("A" * 11, 1, 10)
        assert "максимум" in str(exc_info.value)
