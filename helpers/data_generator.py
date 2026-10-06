import random
import string


def generate_random_string(length: int = 10) -> str:
    """Генерирует случайную строку из букв нижнего регистра."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_email() -> str:
    """Генерирует уникальный email."""
    return f"test_{generate_random_string(8)}@yandex.ru"


def generate_password() -> str:
    """Генерирует пароль."""
    return generate_random_string(10)


def generate_name() -> str:
    """Генерирует имя."""
    return generate_random_string(8).capitalize()


def generate_user_data() -> dict:
    """Генерирует полные данные пользователя."""
    return {
        "email": generate_email(),
        "password": generate_password(),
        "name": generate_name()
    }